#!/bin/bash

# Post-install script to install Docker and setup Jupyter components

set -e

# Install system packages
apt-get update && apt-get install -y git python-minimal

PYDATA_DIR="$HOME/pydata2016"

# Clone PyData repo
git clone --depth 1 https://github.com/jupyter-resources/tutorial-dashboards-declarativewidgets "$PYDATA_DIR" || true

# Install Docker components
"$PYDATA_DIR"/setup/install-docker.sh >> install-docker.log 2>&1 

# Build and run Jupyter components
"$PYDATA_DIR"/setup/setup-jupyter.sh >> setup-jupyter.log 2>&1

# Copy sample notebooks
"$PYDATA_DIR"/setup/copy-notebooks.sh "$PYDATA_DIR/notebooks" >> copy-notebooks.log 2>&1
