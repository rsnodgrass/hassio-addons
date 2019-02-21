#!/bin/bash

cd lutron-radiora1

# Default build is based on homeassistant/amd64-base:latest
docker build -t local/lutron-radiora1 .

# To specify a different platform, set build-arg to a different base image:
# homeassistant/armhf-base
# homeassistant/amd64-base
# homeassistant/aarch64-base
# homeassistant/i386-base

#docker build --build-arg BUILD_FROM="homeassistant/amd64-base:latest" -t local/lutron-radiora1 .
