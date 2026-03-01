# Prek Setup Guide

This project uses `prek`, the Rust implementation of pre-commit, for code linting and formatting.

## Installation

### Prerequisites

- Rust/Cargo (for installing prek)
- Node.js/npm (for prettier)

### Install prek and set up hooks

```bash
# Install prek and set up hooks
make prek-install-hooks

# Or manually:
cargo install prek
prek install
```

## Usage

### Run linters on all files

```bash
make lint
# or
prek run --all-files
```

### Format code

```bash
make format
```

### Run before committing

Prek will automatically run the configured hooks before each commit once installed.

## What's included

- **ruff**: Python linting and formatting
- **prettier**: YAML, Markdown, and JSON formatting
- **pre-commit-hooks**: Basic file checks (trailing whitespace, end-of-file-fixer, etc.)
- **check-github-workflows**: Validates GitHub Actions workflows

## Manual override

To commit without running hooks (not recommended):

```bash
git commit --no-verify
```
