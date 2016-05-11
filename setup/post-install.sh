#!/bin/bash

# Post-install script to install Docker and setup Jupyter components

set -e

PYDATA_DIR="$HOME/pydata2016"

# Clone PyData repo
git clone --depth 1 https://github.com/ibm-et/pydata2016 "$PYDATA_DIR"

# Install Docker components
"$PYDATA_DIR"/setup/install-docker.sh

# Build and run Jupyter components
"$PYDATA_DIR"/setup/setup-jupyter.sh

# Copy sample notebooks
"$PYDATA_DIR"/setup/copy-notebooks.sh "$PYDATA_DIR/notebooks"
