import unittest
from codex.extractor import CodexExtractor

class TestCodexExtractor(unittest.TestCase):
    def test_basic_function(self):
        code = "def hello(name: str) -> None: print(name)"
        extractor = CodexExtractor(code, "test.py")
        m = extractor.extract()
        self.assertEqual(len(m.functions), 1)
        self.assertEqual(m.functions[0].name, "hello")
        self.assertIn("def hello(name: str) -> None:", m.functions[0].signature)

    def test_nested_functions(self):
        code = """
def outer():
    def inner():
        pass
"""
        extractor = CodexExtractor(code, "test.py")
        m = extractor.extract()
        self.assertEqual(len(m.functions), 1)
        self.assertEqual(len(m.functions[0].nested_functions), 1)
        self.assertEqual(m.functions[0].nested_functions[0].name, "inner")

    def test_class_methods(self):
        code = """
class MyClass:
    def my_method(self):
        pass
"""
        extractor = CodexExtractor(code, "test.py")
        m = extractor.extract()
        self.assertEqual(len(m.classes), 1)
        # Regression test: check methods are in nested_functions and redundancy is removed
        self.assertEqual(len(m.classes[0].nested_functions), 1)
        self.assertEqual(m.classes[0].nested_functions[0].name, "my_method")
        self.assertFalse(hasattr(m.classes[0], "methods"))

    def test_nested_classes(self):
        code = """
class Outer:
    class Inner:
        pass
"""
        extractor = CodexExtractor(code, "test.py")
        m = extractor.extract()
        self.assertEqual(len(m.classes), 1)
        self.assertEqual(len(m.classes[0].nested_classes), 1)
        self.assertEqual(m.classes[0].nested_classes[0].name, "Inner")

    def test_complex_imports(self):
        code = "from typing import List as L, Dict as D"
        extractor = CodexExtractor(code, "test.py")
        m = extractor.extract()
        self.assertEqual(len(m.imports), 1)
        self.assertEqual(m.imports[0].module, "typing")
        self.assertEqual(m.imports[0].items[0].name, "List")
        self.assertEqual(m.imports[0].items[0].alias, "L")

    def test_syntax_error_graceful_fail(self):
        code = "def incomplete("
        extractor = CodexExtractor(code, "test.py")
        m = extractor.extract()
        self.assertEqual(len(m.functions), 0)

if __name__ == "__main__":
    unittest.main()
