import json
from typing import List, Dict, Any
from .models import ModuleMap, ClassDef, FunctionDef

class CodexFormatter:
    @staticmethod
    def to_json(maps: List[ModuleMap]) -> str:
        def serializer(obj: Any) -> Any:
            if hasattr(obj, "__dict__"):
                return obj.__dict__
            return str(obj)
        return json.dumps([m for m in maps], default=serializer, indent=2)

    @staticmethod
    def to_markdown(maps: List[ModuleMap]) -> str:
        lines = ["# Codex-Py Structural Map", ""]
        
        for m in maps:
            lines.append(f"## File: `{m.path}`")
            lines.append("")
            
            if m.imports:
                lines.append("### Imports")
                lines.append("```python")
                for imp in m.imports:
                    if imp.module:
                        names = ", ".join(imp.names)
                        lines.append(f"from {imp.module} import {names}")
                    else:
                        lines.append(f"import {imp.names[0]}")
                lines.append("```")
                lines.append("")

            if m.classes:
                for cls in m.classes:
                    lines.append(f"### Class: `{cls.name}`")
                    lines.append("```python")
                    for dec in cls.decorators:
                        lines.append(dec)
                    bases = f"({', '.join(cls.bases)})" if cls.bases else ""
                    lines.append(f"class {cls.name}{bases}:")
                    if cls.docstring:
                        lines.append(f"    \"\"\"{cls.docstring}\"\"\"")
                    
                    for meth in cls.methods:
                        for dec in meth.decorators:
                            lines.append(f"    {dec}")
                        lines.append(f"    {meth.signature}")
                        if meth.docstring:
                            lines.append(f"        \"\"\"{meth.docstring}\"\"\"")
                        lines.append("        ...")
                        lines.append("")
                    
                    if not cls.methods and not cls.docstring:
                        lines.append("    pass")
                    lines.append("```")
                    lines.append("")

            if m.functions:
                lines.append("### Global Functions")
                lines.append("```python")
                for func in m.functions:
                    for dec in func.decorators:
                        lines.append(dec)
                    lines.append(func.signature)
                    if func.docstring:
                        lines.append(f"    \"\"\"{func.docstring}\"\"\"")
                    lines.append("    ...")
                    lines.append("")
                lines.append("```")
                lines.append("")
                
        return "\n".join(lines)
