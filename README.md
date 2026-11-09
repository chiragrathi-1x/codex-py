# Codex-Py

**Codex-Py** is a static analysis tool that extracts implementation-free structural maps of Python codebases. It is designed to provide high-fidelity context for developers and LLMs by stripping away function bodies and logic while preserving class structures, method signatures, type hints, and docstrings.

## The Problem

Large codebases often exceed LLM context windows or overwhelm developers trying to understand a new architecture. Codex-Py bridges this gap by providing a structural "interface" of your project, allowing you to share the what and how without the thousands of lines of implementation details.

## Features

- **AST-Based Extraction**: Prunes function implementations while preserving signatures, decorators, and return types.
- **Gitignore Integration**: Automatically detects and respects `.gitignore` rules to keep your maps clean.
- **Granular Filtering**: Include or exclude private members (those prefixed with underscores) or specific module paths.
- **Multi-Format Output**: Generate structured Markdown or JSON.
- **Modern Python Support**: Full support for Type Hints, `async/await`, and complex nested structures.
- **Token-Awareness**: Provides heuristics for token usage estimation.

## Installation

```bash
git clone https://github.com/username/codex-py.git
cd codex-py
pip install .
```

## CLI Usage

- **Basic scan of current directory:**
  ```bash
  codex .
  ```

- **Save to a file, excluding private methods:**
  ```bash
  codex . --output context.md --no-private
  ```

- **Limit recursion depth and exclude specific folders:**
  ```bash
  codex ./src --depth 2 --exclude "**/tests/*" --exclude "docs/*"
  ```

- **Export to JSON for programmatic use:**
  ```bash
  codex ./app --format json
  ```

## Limitations

- **Static Only**: Codex-Py uses the standard `ast` module. It does not execute code, meaning it cannot resolve attributes created dynamically at runtime (e.g., via `setattr` or complex metaclass logic).
- **Syntax Specific**: It requires syntactically valid Python 3.10+ code. Files with syntax errors are skipped.
- **Comment Pruning**: Regular code comments are stripped; only docstrings (string literals at the start of blocks) are preserved if requested.

## Testing

Run the test suite using `unittest`:

```bash
python -m unittest discover tests
```