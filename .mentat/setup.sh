#!/bin/bash

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH for this session
export PATH="$HOME/.local/bin:$PATH"

# Install project dependencies
poetry install
