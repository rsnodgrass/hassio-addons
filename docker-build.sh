#!/bin/bash

#for ADDON in virtual-ip2sl xantech-serial-bridge radiora-classic-bridge
for ADDON in keepalived virtual-ip2sl
do
    pushd $ADDON
    #docker build --build-arg BUILD_FROM="hassioaddons/base:2.3.1" -t $ADDON .
    docker build --build-arg BUILD_FROM="python:3.12-alpine" -t $ADDON .
    popd

# To specify a different Home Assistant platform, set build-arg to a different base image:
#   docker build --build-arg BUILD_FROM="homeassistant/amd64-base:latest" -t $ADDON .
#
#   homeassistant/amd64-base (default)
#   homeassistant/armhf-base
#   homeassistant/aarch64-base
#   homeassistant/i386-base
