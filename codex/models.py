from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ImportItem:
    name: str
    alias: Optional[str] = None

@dataclass
class ImportDef:
    module: Optional[str]
    items: List[ImportItem] = field(default_factory=list)

@dataclass
class FunctionDef:
    name: str
    signature: str
    docstring: Optional[str]
    is_async: bool
    decorators: List[str] = field(default_factory=list)
    is_private: bool = False
    nested_functions: List['FunctionDef'] = field(default_factory=list)

@dataclass
class ClassDef:
    name: str
    bases: List[str]
    docstring: Optional[str]
    decorators: List[str] = field(default_factory=list)
    is_private: bool = False
    nested_classes: List['ClassDef'] = field(default_factory=list)
    nested_functions: List[FunctionDef] = field(default_factory=list)

@dataclass
class ModuleMap:
    path: str
    imports: List[ImportDef] = field(default_factory=list)
    classes: List[ClassDef] = field(default_factory=list)
    functions: List[FunctionDef] = field(default_factory=list)
