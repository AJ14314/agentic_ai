# Pre-commit Hooks Setup

This document outlines the setup and usage of pre-commit hooks for this project, specifically for Black code formatting.

## Installation

1. Install pre-commit:
```bash
pip install pre-commit
```

2. Install Black with Jupyter notebook support:
```bash
pip install black[jupyter]
```

## Configuration

### .pre-commit-config.yaml
The project uses the following pre-commit configuration:

```yaml
repos:
-   repo: https://github.com/psf/black
    rev: 24.2.0
    hooks:
    -   id: black
        language_version: python3
        types_or: [python, jupyter]
        additional_dependencies: ["black[jupyter]"]
```

This configuration:
- Uses Black version 24.2.0
- Targets Python 3
- Formats both Python and Jupyter notebook files
- Includes Jupyter notebook support through the additional dependency

## Setup Steps

1. Install the required packages:
```bash
pip install pre-commit black[jupyter]
```

2. Install pre-commit hooks:
```bash
pre-commit install
```

## Usage

### Automatic Formatting
The pre-commit hooks will automatically run Black when:
- You make a git commit
- You can also run them manually on all files

### Manual Usage

Run pre-commit on all files:
```bash
pre-commit run --all-files
```

Run pre-commit on staged files:
```bash
pre-commit run
```

### Common Commands

1. Check pre-commit version:
```bash
pre-commit --version
```

2. Update pre-commit hooks:
```bash
pre-commit autoupdate
```

3. Clean pre-commit cache:
```bash
pre-commit clean
```

## Troubleshooting

If you encounter any issues:

1. Check the pre-commit log:
```bash
cat ~/.cache/pre-commit/pre-commit.log
```

2. Verify the configuration:
```bash
pre-commit check
```

3. Try running with verbose output:
```bash
pre-commit run --verbose
```

4. If you get YAML syntax errors:
- Make sure all dependencies are properly quoted
- Check for proper indentation
- Verify that list items are properly formatted

## Best Practices

1. Always commit your `.pre-commit-config.yaml` file
2. Keep the pre-commit hooks up to date
3. Run pre-commit checks before pushing code
4. Use the same pre-commit configuration across your team

## Additional Resources

- [Pre-commit Documentation](https://pre-commit.com/)
- [Black Documentation](https://black.readthedocs.io/)
- [Jupyter Notebook Formatting](https://black.readthedocs.io/en/stable/usage_and_configuration/file_collection_and_discovery.html#jupyter-notebooks)