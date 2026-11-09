class CodexTokenizer:
    @staticmethod
    def estimate_tokens(content: str) -> int:
        if not content:
            return 0
        return max(1, int(len(content) / 3.7))
