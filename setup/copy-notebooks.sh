#!/bin/bash

# Copy notebooks from source directory to Docker volume directory

USAGE="Usage: `basename $0` src_dir"

SRC=$1 && [ -z "$SRC" ] && echo "$USAGE" && exit 85

# jovyan user
: ${USER_PID:=1000}

# Determine Docker volume
VOLUME=$(docker volume ls | grep -o "dockerdeploy.*")

# Identify host directory backing the volume
HOST_DIR=$(docker volume inspect -f '{{.Mountpoint}}' "$VOLUME")

# Copy notebooks and set permissions
cp -R "$SRC"/* "$HOST_DIR"
chown -R $USER_PID:users "$HOST_DIR"
