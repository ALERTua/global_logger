#!/bin/bash

# Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"

# Format code with ruff
poetry run ruff format .

# Fix linting issues with ruff
poetry run ruff check --fix .

# Validate pyproject.toml
poetry check
