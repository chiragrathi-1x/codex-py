import fnmatch
from pathlib import Path
from typing import List

class IgnoreHandler:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.patterns = [".git/", "__pycache__/", "*.pyc", "*.pyo", "*.pyd"]
        self._load_gitignore()

    def _load_gitignore(self) -> None:
        gitignore_path = self.root_dir / ".gitignore"
        if gitignore_path.exists():
            with open(gitignore_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Ensure directory patterns end with * for fnmatch
                        if line.endswith("/"):
                            self.patterns.append(line + "*")
                        self.patterns.append(line)

    def is_ignored(self, path: Path) -> bool:
        # Get path relative to root for matching
        try:
            rel_path = str(path.relative_to(self.root_dir))
        except ValueError:
            rel_path = str(path)

        for pattern in self.patterns:
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(path.name, pattern):
                return True
            # Handle recursive directory patterns
            if "/" in pattern and rel_path.startswith(pattern.rstrip("*")):
                return True
        return False
