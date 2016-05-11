#!/bin/bash

set -e

# Install Docker Engine
sudo curl -fsSL https://get.docker.com/ | sh
sudo service docker start || true
sudo docker run hello-world

# Install docker-compose as a Docker container
sudo curl -L https://github.com/docker/compose/releases/download/1.7.1/run.sh \
  > /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
