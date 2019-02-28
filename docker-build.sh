#!/bin/bash

cd radiora-classic-bridge
docker build --build-arg BUILD_FROM="python:3.6-alpine" -t radiora-classic-bridge .

#docker build --build-arg BUILD_FROM="hassioaddons/base:2.3.1" -t radiora-classic-bridge .

# To specify a different Home Assistant platform, set build-arg to a different base image:
#   docker build --build-arg BUILD_FROM="homeassistant/amd64-base:latest" -t radiora-classic-bridge .
#
# homeassistant/amd64-base (default)
# homeassistant/armhf-base
# homeassistant/aarch64-base
# homeassistant/i386-base
