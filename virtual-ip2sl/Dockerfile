#ARG BUILD_FROM=hassioaddons/base
ARG BUILD_FROM=jfloff/alpine-python:3.6-onbuild
FROM $BUILD_FROM

ARG BUILD_ARCH
ARG BUILD_VERSION
ARG APP_DIR="/app"

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
 && pip3 install --no-cache-dir -r "${APP_DIR}/dependencies" \
 && rm -rf /root/.cache /var/cache

COPY . $APP_DIR

EXPOSE 80
EXPOSE 4998
EXPOSE 4999
EXPOSE 5000
EXPOSE 5001
EXPOSE 5002
EXPOSE 5003
EXPOSE 5004
EXPOSE 5005
EXPOSE 5006
EXPOSE 5007
EXPOSE 9131

WORKDIR $APP_DIR
CMD [ "python3", "server.py" ]
