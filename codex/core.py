from pathlib import Path
from typing import List, Optional
from .ignore_handler import IgnoreHandler
from .extractor import CodexExtractor
from .models import ModuleMap

class CodexCore:
    def __init__(self,
                 root_path: str,
                 include_private: bool = True,
                 include_docstrings: bool = True,
                 exclude_patterns: Optional[List[str]] = None,
                 depth: Optional[int] = None):
        self.root_path = Path(root_path).resolve()
        self.include_private = include_private
        self.include_docstrings = include_docstrings
        self.exclude_patterns = exclude_patterns or []
        self.depth = depth
        self.ignore_handler = IgnoreHandler(self.root_path)

    def _should_process(self, path: Path, current_depth: int) -> bool:
        if self.depth is not None and current_depth > self.depth:
            return False
        if self.ignore_handler.is_ignored(path):
            return False
        # Custom excludes
        import fnmatch
        rel_path = str(path.relative_to(self.root_path))
        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(path.name, pattern):
                return False
        return True

    def run(self) -> List[ModuleMap]:
        results = []
        for py_file in self.root_path.rglob("*.py"):
            # Calculate depth
            rel_parts = py_file.relative_to(self.root_path).parts
            current_depth = len(rel_parts) - 1

            if not self._should_process(py_file, current_depth):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    source = f.read()
                
                extractor = CodexExtractor(
                    source=source,
                    path=str(py_file.relative_to(self.root_path)),
                    include_private=self.include_private,
                    include_docstrings=self.include_docstrings
                )
                results.append(extractor.extract())
            except Exception as e:
                # Skip files that can't be read or parsed
                continue
        
        return sorted(results, key=lambda x: x.path)
