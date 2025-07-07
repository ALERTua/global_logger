#!/bin/bash

# Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"

# Format code with ruff
ruff format .

# Fix linting issues with ruff
ruff check --fix .

# Validate pyproject.toml
poetry check
