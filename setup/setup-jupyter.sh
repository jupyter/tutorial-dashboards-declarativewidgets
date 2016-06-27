#!/bin/bash

set -e

# Clone dashboards setup repo
git clone https://github.com/jupyter-incubator/dashboards_setup.git \
  --depth 1 || true
  
# Fetch pre-assigned credentials from user metadata
SETUP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python "${SETUP_DIR}/setup-credentials.py"

# Build and run jupyter/notebook, jupyter/dashboards_server, and
# jupyter/kernel_gateway in Docker containers.
pushd dashboards_setup/docker_deploy
docker-compose up -d --build
popd