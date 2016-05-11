#!/bin/bash

set -e

# Clone dashboards setup repo
git clone https://github.com/jupyter-incubator/dashboards_setup.git \
  --depth 1 || true

# Build and run jupyter/notebook, jupyter/dashboards_server, and
# jupyter/kernel_gateway in Docker containers.
cd dashboards_setup/docker_deploy && \
   docker-compose up -d --build && \
   cd -
