import json
from typing import List, Dict, Any
from .models import ModuleMap, ClassDef, FunctionDef

class CodexFormatter:
    @staticmethod
    def to_json(maps: List[ModuleMap]) -> str:
        def serializer(obj: Any) -> Any:
            if hasattr(obj, "__dict__"):
                return {k: v for k, v in obj.__dict__.items()}
            return str(obj)
        return json.dumps([m for m in maps], default=serializer, indent=2)

    @staticmethod
    def to_markdown(maps: List[ModuleMap]) -> str:
        lines = ["# Codex-Py Structural Map", ""]
        
        def render_func(func: FunctionDef, indent: str):
            for dec in func.decorators:
                lines.append(f"{indent}{dec}")
            lines.append(f"{indent}{func.signature}")
            if func.docstring:
                ds = func.docstring.strip().replace("\n", f"\n{indent}    ")
                lines.append(f"{indent}    \"\"\"{ds}\"\"\"")
            
            if func.nested_functions:
                for nf in func.nested_functions:
                    render_func(nf, indent + "    ")
            else:
                lines.append(f"{indent}    ...")
            lines.append("")

        def render_class(cls: ClassDef, indent: str):
            for dec in cls.decorators:
                lines.append(f"{indent}{dec}")
            bases = f"({', '.join(cls.bases)})" if cls.bases else ""
            lines.append(f"{indent}class {cls.name}{bases}:")
            if cls.docstring:
                ds = cls.docstring.strip().replace("\n", f"\n{indent}    ")
                lines.append(f"{indent}    \"\"\"{ds}\"\"\"")
            
            has_content = False
            for nf in cls.nested_functions:
                render_func(nf, indent + "    ")
                has_content = True
            for nc in cls.nested_classes:
                render_class(nc, indent + "    ")
                has_content = True
            
            if not has_content and not cls.docstring:
                lines.append(f"{indent}    pass")
            lines.append("")

        for m in maps:
            lines.append(f"## File: `{m.path}`")
            lines.append("")
            
            if m.imports:
                lines.append("### Imports")
                lines.append("```python")
                for imp in m.imports:
                    parts = []
                    for it in imp.items:
                        part = it.name
                        if it.alias:
                            part += f" as {it.alias}"
                        parts.append(part)
                    
                    if imp.module:
                        lines.append(f"from {imp.module} import {', '.join(parts)}")
                    else:
                        lines.append(f"import {', '.join(parts)}")
                lines.append("```")
                lines.append("")

            if m.classes or m.functions:
                lines.append("### Structure")
                lines.append("```python")
                for cls in m.classes:
                    render_class(cls, "")
                for func in m.functions:
                    render_func(func, "")
                lines.append("```")
                lines.append("")
                
        return "\n".join(lines).replace("\n\n\n", "\n\n")
