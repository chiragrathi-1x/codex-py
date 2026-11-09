from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ImportDef:
    module: Optional[str]
    names: List[str]
    alias: Optional[str] = None

@dataclass
class FunctionDef:
    name: str
    signature: str
    docstring: Optional[str]
    is_async: bool
    decorators: List[str] = field(default_factory=list)
    is_private: bool = False

@dataclass
class ClassDef:
    name: str
    bases: List[str]
    docstring: Optional[str]
    methods: List[FunctionDef] = field(default_factory=list)
    decorators: List[str] = field(default_factory=list)
    is_private: bool = False

@dataclass
class ModuleMap:
    path: str
    imports: List[ImportDef] = field(default_factory=list)
    classes: List[ClassDef] = field(default_factory=list)
    functions: List[FunctionDef] = field(default_factory=list)
