import ast
from typing import List, Optional, Union
from .models import ModuleMap, ClassDef, FunctionDef, ImportDef

class CodexExtractor(ast.NodeVisitor):
    def __init__(self, source: str, path: str, include_private: bool = True, include_docstrings: bool = True):
        self.source = source
        self.path = path
        self.include_private = include_private
        self.include_docstrings = include_docstrings
        self.module_map = ModuleMap(path=path)
        self._current_class: Optional[ClassDef] = None

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
        # Create a dummy node to unparse only the signature
        # We can't easily unparse just the header in stdlib ast,
        # so we reconstruct it or use a trick.
        args = ast.unparse(node.args)
        returns = f" -> {ast.unparse(node.returns)}" if node.returns else ""
        prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
        return f"{prefix} {node.name}({args}){returns}:"

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.module_map.imports.append(ImportDef(module=None, names=[alias.name], alias=alias.asname))

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module = ("." * (node.level or 0)) + (node.module or "")
        names = [alias.name for alias in node.names]
        self.module_map.imports.append(ImportDef(module=module, names=names))

    def visit_ClassDef(self, node: ast.ClassDef):
        is_private = self._is_private(node.name)
        if not self.include_private and is_private:
            return

        bases = [ast.unparse(b) for b in node.bases]
        class_def = ClassDef(
            name=node.name,
            bases=bases,
            docstring=self._get_docstring(node),
            decorators=self._get_decorators(node),
            is_private=is_private
        )

        old_class = self._current_class
        self._current_class = class_def
        self.generic_visit(node)
        self._current_class = old_class

        if old_class is None:
            self.module_map.classes.append(class_def)

    def _handle_function(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]):
        is_private = self._is_private(node.name)
        if not self.include_private and is_private:
            return

        func_def = FunctionDef(
            name=node.name,
            signature=self._get_signature(node),
            docstring=self._get_docstring(node),
            is_async=is_async := isinstance(node, ast.AsyncFunctionDef),
            decorators=self._get_decorators(node),
            is_private=is_private
        )

        if self._current_class:
            self._current_class.methods.append(func_def)
        else:
            self.module_map.functions.append(func_def)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._handle_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._handle_function(node)

    def extract(self) -> ModuleMap:
        try:
            tree = ast.parse(self.source)
            self.visit(tree)
        except SyntaxError:
            # If a file has syntax errors, we return the map as-is (likely empty or partial)
            pass
        return self.module_map
