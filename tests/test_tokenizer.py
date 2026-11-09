import unittest
from codex.tokenizer import CodexTokenizer

class TestCodexTokenizer(unittest.TestCase):
    def test_estimate_tokens_empty(self):
        self.assertEqual(CodexTokenizer.estimate_tokens(""), 0)

    def test_estimate_tokens_logic(self):
        content = "A" * 37
        # 37 / 3.7 = 10
        self.assertEqual(CodexTokenizer.estimate_tokens(content), 10)

    def test_estimate_tokens_minimum(self):
        self.assertEqual(CodexTokenizer.estimate_tokens("x"), 1)

if __name__ == "__main__":
    unittest.main()