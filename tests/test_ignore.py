import unittest
from pathlib import Path
import tempfile
import shutil
from codex.ignore_handler import IgnoreHandler

class TestIgnoreHandler(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        (self.test_dir / ".gitignore").write_text("*.log\ntemp/\n!keep.log", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_ignore_file(self):
        handler = IgnoreHandler(self.test_dir)
        self.assertTrue(handler.is_ignored(self.test_dir / "error.log"))
        self.assertFalse(handler.is_ignored(self.test_dir / "main.py"))

    def test_negation(self):
        handler = IgnoreHandler(self.test_dir)
        self.assertFalse(handler.is_ignored(self.test_dir / "keep.log"))

    def test_ignore_dir(self):
        handler = IgnoreHandler(self.test_dir)
        d = self.test_dir / "temp"
        d.mkdir()
        self.assertTrue(handler.is_ignored(d))
        self.assertTrue(handler.is_ignored(d / "cache.py"))

if __name__ == "__main__":
    unittest.main()
