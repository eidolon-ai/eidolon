#!/bin/bash

# Get the directory of the pyproject.toml file
DIR=$1

# Extract the package name and current version from the pyproject.toml file
PACKAGE_NAME=$(grep -m 1 '^name = ' $DIR/pyproject.toml | awk -F '"' '{print $2}')
CURRENT_VERSION=$(grep -m 1 '^version = ' $DIR/pyproject.toml | awk -F '"' '{print $2}')

# Check if the current version of the package is published on PyPI
if ! pip index versions $PACKAGE_NAME 2>/dev/null | grep -q $CURRENT_VERSION; then
    echo "Version $CURRENT_VERSION of $PACKAGE_NAME is not published on PyPI. Publishing now..."
else
    echo "Version $CURRENT_VERSION of $PACKAGE_NAME is already published on PyPI."
fi
