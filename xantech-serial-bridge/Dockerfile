#ARG BUILD_FROM=hassioaddons/base
ARG BUILD_FROM=jfloff/alpine-python:3.6-onbuild
FROM $BUILD_FROM

ARG BUILD_ARCH
ARG BUILD_VERSION

LABEL authors="Ryan Snodgrass"

# install git and Python3 environment
RUN apk update \
 && apk add --no-cache bash git python3 \
 && python3 -m ensurepip \
 && rm -r /usr/lib/python*/ensurepip \
 && pip3 install --upgrade pip setuptools \
 && cd /usr/bin \
 && ln -sf pip3 pip \
 && ln -sf python3 python \
 $$ pip3 install --no-cache-dir -r "${APP_DIR}/dependencies"
 && rm -rf /root/.cache /var/cache

ARG APP_DIR="/app"
COPY . $APP_DIR

EXPOSE 5000

WORKDIR $APP_DIR
CMD [ "python3", "bridge" ]
