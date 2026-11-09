import unittest
from pathlib import Path
import tempfile
import shutil
from codex.core import CodexCore

class TestCodexCore(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        (self.test_dir / "src").mkdir()
        (self.test_dir / "src" / "a.py").write_text("def a(): pass", encoding="utf-8")
        (self.test_dir / "src" / "_b.py").write_text("def b(): pass", encoding="utf-8")
        (self.test_dir / "tests").mkdir()
        (self.test_dir / "tests" / "test_a.py").write_text("def test_a(): pass", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_run_recursive(self):
        core = CodexCore(str(self.test_dir))
        results = core.run()
        # Should find 3 files
        self.assertEqual(len(results), 3)

    def test_exclude_patterns(self):
        core = CodexCore(str(self.test_dir), exclude_patterns=["tests/*"])
        results = core.run()
        self.assertEqual(len(results), 2)
        for r in results:
            self.assertFalse(r.path.startswith("tests"))

    def test_depth_limit(self):
        core = CodexCore(str(self.test_dir), depth=0)
        results = core.run()
        # No files in root dir, all are in subdirs
        self.assertEqual(len(results), 0)

if __name__ == "__main__":
    unittest.main()