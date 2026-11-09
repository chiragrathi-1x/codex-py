import fnmatch
from pathlib import Path
from typing import List, Tuple

class IgnoreHandler:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.rules: List[Tuple[str, bool, bool]] = [
            (".git", False, True),
            ("__pycache__", False, True),
            ("*.pyc", False, False),
            ("*.pyo", False, False),
            ("*.pyd", False, False),
        ]
        self._load_gitignore()

    def _load_gitignore(self) -> None:
        gitignore_path = self.root_dir / ".gitignore"
        if gitignore_path.exists():
            try:
                with open(gitignore_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        
                        negation = line.startswith("!")
                        if negation:
                            line = line[1:]
                        
                        dir_only = line.endswith("/")
                        if dir_only:
                            line = line[:-1]
                        
                        self.rules.append((line, negation, dir_only))
            except Exception:
                pass

    def is_ignored(self, path: Path) -> bool:
        try:
            rel_path = path.relative_to(self.root_dir)
        except ValueError:
            return False

        rel_str = str(rel_path).replace("\\", "/")
        if not rel_str or rel_str == ".":
            return False

        ignored = False
        for pattern, negation, dir_only in self.rules:
            if dir_only and not path.is_dir():
                continue
            
            match = False
            if "/" in pattern:
                if fnmatch.fnmatch(rel_str, pattern) or fnmatch.fnmatch(rel_str, pattern + "/*"):
                    match = True
            else:
                if fnmatch.fnmatch(path.name, pattern):
                    match = True
            
            if match:
                ignored = not negation
        
        return ignored
