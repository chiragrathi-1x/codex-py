import argparse
import sys
from pathlib import Path
from .core import CodexCore
from .formatter import CodexFormatter
from .tokenizer import CodexTokenizer

def main():
    parser = argparse.ArgumentParser(
        prog="codex",
        description="Codex-Py: Structural codebase mapping for documentation and LLMs."
    )
    parser.add_argument("path", help="Directory to analyze (default: current)", default=".", nargs="?")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--format", "-f", choices=["markdown", "json"], default="markdown", help="Output format")
    parser.add_argument("--no-private", action="store_false", dest="include_private", help="Exclude private members (starting with _)")
    parser.add_argument("--no-docstrings", action="store_false", dest="include_docstrings", help="Exclude docstrings")
    parser.add_argument("--depth", type=int, help="Maximum directory recursion depth")
    parser.add_argument("--exclude", action="append", help="Glob patterns to exclude")
    
    args = parser.parse_args()

    core = CodexCore(
        root_path=args.path,
        include_private=args.include_private,
        include_docstrings=args.include_docstrings,
        exclude_patterns=args.exclude,
        depth=args.depth
    )

    try:
        module_maps = core.run()
    except Exception as e:
        print(f"Error scanning directory: {e}", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        output = CodexFormatter.to_json(module_maps)
    else:
        output = CodexFormatter.to_markdown(module_maps)

    token_estimate = CodexTokenizer.estimate_tokens(output)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Successfully wrote map to {args.output} (~{token_estimate} tokens)")
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output)
        print(f"\n--- Token Estimate: ~{token_estimate} tokens ---", file=sys.stderr)

if __name__ == "__main__":
    main()
