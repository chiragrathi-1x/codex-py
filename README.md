# Codex-Py

**Codex-Py** is a static analysis tool that extracts implementation-free structural maps of Python codebases. It is designed to provide high-fidelity context for developers and LLMs by stripping away function bodies and logic while preserving class structures, method signatures, type hints, and docstrings.

## The Problem

Large codebases often exceed LLM context windows or overwhelm developers trying to understand a new architecture. Existing solutions usually offer a binary choice: provide the entire source (which consumes too many tokens) or a simple file tree (which lacks enough detail). Codex-Py bridges this gap by providing a structural "interface" of your project.

## Features

- **AST-Based Extraction**: Prunes function implementations while meticulously preserving signatures, decorators, and return types.
- **Gitignore Integration**: Automatically detects and respects `.gitignore` rules to keep your maps clean of artifacts and virtual environments.
- **Granular Filtering**: Include or exclude private members (those prefixed with underscores) or specific module paths.
- **Multi-Format Output**: Generate structured Markdown for human readability or JSON for integration into other automated pipelines.
- **Modern Python Support**: Full support for Type Hints, `async/await` syntax, and complex nested structures.
- **Token-Awareness**: Includes logic to estimate the token footprint of the generated map.

## Installation

As Codex-Py is currently in development, you can install it from source:

```bash
git clone https://github.com/username/codex-py.git
cd codex-py
pip install .
```

## Quick Start

Generate a structural map of your current directory:

```bash
codex .
```

## CLI Examples

- **Save to a file, excluding private methods:**
  ```bash
  codex . --output context.md --no-private
  ```

- **Limit recursion depth and include docstrings:**
  ```bash
  codex ./src --depth 2 --include-docstrings
  ```

- **Export to JSON for programmatic use:**
  ```bash
  codex ./app --format json --exclude 'tests/*'
  ```

## Limitations

- **Static Analysis**: Codex-Py performs static analysis using the `ast` module. It does not execute code and cannot resolve dynamic runtime attributes or meta-programming results.
- **Import Resolution**: While it maps dependencies, it does not currently verify if those imports are valid or installed in the environment.

## Contributing

Contributions are welcome! Please ensure that any new features include corresponding updates to the test suite and adhere to the project's quality standards. Codex-Py aims for 100% coverage of Python 3.10+ syntax features.