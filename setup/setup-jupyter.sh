#!/bin/bash

set -e

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Clone dashboards setup repo
git clone https://github.com/jupyter-incubator/dashboards_setup.git \
  --depth 1 || true
  
pushd dashboards_setup/docker_deploy
# Fetch pre-assigned credentials from user metadata
python "${MY_DIR}/setup-credentials.py"
# Build and run jupyter/notebook, jupyter/dashboards_server, and
# jupyter/kernel_gateway in Docker containers.
docker-compose up -d --build
popd