class CodexTokenizer:
    @staticmethod
    def estimate_tokens(content: str) -> int:
        """
        Rough estimation of token count for LLMs (GPT-style).
        Uses a heuristic of ~4 characters per token.
        """
        if not content:
            return 0
        # Standard heuristic for code/English mix
        return max(1, int(len(content) / 3.7))
