#!/bin/bash

cd radiora-classic-bridge
docker build -t radiora-classic-bridge .

# docker run radiora-classic-bridge

# To specify a different platform, set build-arg to a different base image:
#   docker build --build-arg BUILD_FROM="homeassistant/amd64-base:latest" -t radiora-classic-bridge .
#
# homeassistant/amd64-base (default)
# homeassistant/armhf-base
# homeassistant/aarch64-base
# homeassistant/i386-base
