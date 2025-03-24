import unittest
from src.summarize import summarize_code

class TestSummarizeCode(unittest.TestCase):
    def test_summarize_code(self):
        code_snippet = "def add(a, b): return a + b"
        summary = summarize_code(code_snippet)
        self.assertIn("function", summary.lower())

if __name__ == "__main__":
    unittest.main()