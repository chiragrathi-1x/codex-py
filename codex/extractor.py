import ast
from typing import List, Optional, Union
from .models import ModuleMap, ClassDef, FunctionDef, ImportDef, ImportItem

class CodexExtractor(ast.NodeVisitor):
    def __init__(self, source: str, path: str, include_private: bool = True, include_docstrings: bool = True):
        self.source = source
        self.path = path
        self.include_private = include_private
        self.include_docstrings = include_docstrings
        self.module_map = ModuleMap(path=path)
        self._scope_stack: List[Union[ModuleMap, ClassDef, FunctionDef]] = [self.module_map]

    def _is_private(self, name: str) -> bool:
        return name.startswith("_") and not (name.startswith("__") and name.endswith("__"))

    def _get_docstring(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module]) -> Optional[str]:
        if not self.include_docstrings:
            return None
        return ast.get_docstring(node)

    def _get_decorators(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]) -> List[str]:
        decorators = []
        for dec in node.decorator_list:
            try:
                decorators.append("@" + ast.unparse(dec))
            except Exception:
                continue
        return decorators

    def _get_signature(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> str:
        args = ast.unparse(node.args)
        returns = f" -> {ast.unparse(node.returns)}" if node.returns else ""
        prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
        return f"{prefix} {node.name}({args}){returns}:"

    def visit_Import(self, node: ast.Import):
        items = [ImportItem(name=alias.name, alias=alias.asname) for alias in node.names]
        self.module_map.imports.append(ImportDef(module=None, items=items))

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module = ("." * (node.level or 0)) + (node.module or "")
        items = [ImportItem(name=alias.name, alias=alias.asname) for alias in node.names]
        self.module_map.imports.append(ImportDef(module=module, items=items))

    def visit_ClassDef(self, node: ast.ClassDef):
        is_private = self._is_private(node.name)
        if not self.include_private and is_private:
            return

        class_def = ClassDef(
            name=node.name,
            bases=[ast.unparse(b) for b in node.bases],
            docstring=self._get_docstring(node),
            decorators=self._get_decorators(node),
            is_private=is_private
        )

        parent = self._scope_stack[-1]
        if isinstance(parent, ModuleMap):
            parent.classes.append(class_def)
        elif isinstance(parent, ClassDef):
            parent.nested_classes.append(class_def)

        self._scope_stack.append(class_def)
        self.generic_visit(node)
        self._scope_stack.pop()

    def _handle_function(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]):
        is_private = self._is_private(node.name)
        if not self.include_private and is_private:
            return

        func_def = FunctionDef(
            name=node.name,
            signature=self._get_signature(node),
            docstring=self._get_docstring(node),
            is_async=isinstance(node, ast.AsyncFunctionDef),
            decorators=self._get_decorators(node),
            is_private=is_private
        )

        parent = self._scope_stack[-1]
        if isinstance(parent, ModuleMap):
            parent.functions.append(func_def)
        elif isinstance(parent, ClassDef):
            parent.nested_functions.append(func_def)
        elif isinstance(parent, FunctionDef):
            parent.nested_functions.append(func_def)

        self._scope_stack.append(func_def)
        self.generic_visit(node)
        self._scope_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._handle_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._handle_function(node)

    def extract(self) -> ModuleMap:
        try:
            tree = ast.parse(self.source)
            self.visit(tree)
        except (SyntaxError, IndentationError):
            pass
        return self.module_map
