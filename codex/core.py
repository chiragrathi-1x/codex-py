from pathlib import Path
from typing import List, Optional
from .ignore_handler import IgnoreHandler
from .extractor import CodexExtractor
from .models import ModuleMap
import fnmatch

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
        
        try:
            rel_path = str(path.relative_to(self.root_path))
        except ValueError:
            rel_path = str(path)

        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(path.name, pattern):
                return False
        return True

    def run(self) -> List[ModuleMap]:
        results = []
        if not self.root_path.exists():
            return []

        def _walk(current_dir: Path, current_depth: int):
            if self.depth is not None and current_depth > self.depth:
                return
            
            if self.ignore_handler.is_ignored(current_dir):
                return

            try:
                for item in sorted(current_dir.iterdir()):
                    if item.is_dir():
                        _walk(item, current_depth + 1)
                    elif item.is_file() and item.suffix == ".py":
                        if self._should_process(item, current_depth):
                            try:
                                with open(item, "r", encoding="utf-8") as f:
                                    source = f.read()
                                
                                extractor = CodexExtractor(
                                    source=source,
                                    path=str(item.relative_to(self.root_path)),
                                    include_private=self.include_private,
                                    include_docstrings=self.include_docstrings
                                )
                                results.append(extractor.extract())
                            except Exception:
                                continue
            except PermissionError:
                pass

        _walk(self.root_path, 0)
        return sorted(results, key=lambda x: x.path)
