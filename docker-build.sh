#!/bin/bash

cd radiora-classic-bridge
docker build -t local/radiora-classic-bridge .

# To specify a different platform, set build-arg to a different base image:
# homeassistant/amd64-base (default)
# homeassistant/armhf-base
# homeassistant/aarch64-base
# homeassistant/i386-base

#docker build --build-arg BUILD_FROM="homeassistant/amd64-base:latest" -t local/radiora-classic-bridge .
