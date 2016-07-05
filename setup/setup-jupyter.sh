#!/bin/bash

set -e

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SHA=241fdda2c7ed1497e3b2e8ccff0f0ac134ab1ea8
PROJECT=dashboards_setup

# Remove existing repo no matter what
rm -rf $PROJECT
# Clone dashboards setup repo
git clone https://github.com/jupyter-incubator/${PROJECT}.git

pushd dashboards_setup/docker_deploy
# Reset to a fixed commit
git reset --hard $SHA 
# Fetch pre-assigned credentials from user metadata
python "${MY_DIR}/setup-credentials.py"
# Build and run jupyter/notebook, jupyter/dashboards_server, and
# jupyter/kernel_gateway in Docker containers.
docker-compose up -d --build
popd