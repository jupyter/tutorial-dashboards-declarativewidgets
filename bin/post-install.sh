#!/bin/bash

# Post-install script to run jupyter/notebook, jupyter/dashboards_server, and
# jupyter/kernel_gateway in Docker containers.

set -e

# Install Docker Engine
sudo curl -fsSL https://get.docker.com/ | sh
sudo service docker start || true
sudo docker run hello-world

# Install docker-compose as a Docker container
sudo curl -L https://github.com/docker/compose/releases/download/1.7.1/run.sh \
  > /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone dashboards setup repo
git clone https://github.com/jupyter-incubator/dashboards_setup.git
cd dashboards_setup

# Start components in Docker containers
cd docker_deploy
docker-compose build
docker-compose up -d
