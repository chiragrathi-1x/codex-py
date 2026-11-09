import unittest
import json
from codex.models import ModuleMap, FunctionDef, ImportDef, ImportItem
from codex.formatter import CodexFormatter

class TestCodexFormatter(unittest.TestCase):
    def setUp(self):
        self.sample_map = ModuleMap(
            path="test.py",
            imports=[ImportDef(module=None, items=[ImportItem("os", "system")])],
            functions=[FunctionDef(name="run", signature="def run():", docstring="Go", is_async=False)]
        )

    def test_markdown_format_with_alias(self):
        output = CodexFormatter.to_markdown([self.sample_map])
        self.assertIn("import os as system", output)

    def test_json_format_recursive(self):
        f1 = FunctionDef(name="f1", signature="def f1():", docstring=None, is_async=False)
        f1.nested_functions = [FunctionDef(name="f2", signature="def f2():", docstring=None, is_async=False)]
        m = ModuleMap(path="a.py", functions=[f1])
        
        output = CodexFormatter.to_json([m])
        data = json.loads(output)
        self.assertEqual(data[0]["functions"][0]["nested_functions"][0]["name"], "f2")

if __name__ == "__main__":
    unittest.main()
