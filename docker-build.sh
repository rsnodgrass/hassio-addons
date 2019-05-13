#!/bin/bash

#export ADDON=radiora-classic-bridge
export ADDON=rs485-pool-controller

pushd $ADDON
docker build --build-arg BUILD_FROM="python:3.6-alpine" -t $ADDON .
popd

#docker build --build-arg BUILD_FROM="hassioaddons/base:2.3.1" -t $ADDON .

# To specify a different Home Assistant platform, set build-arg to a different base image:
#   docker build --build-arg BUILD_FROM="homeassistant/amd64-base:latest" -t $ADDON .
#
#   homeassistant/amd64-base (default)
#   homeassistant/armhf-base
#   homeassistant/aarch64-base
#   homeassistant/i386-base
