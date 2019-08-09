ARG BUILD_FROM=hassioaddons/base
#ARG BUILD_FROM=jfloff/alpine-python:3.6-onbuild
FROM $BUILD_FROM

ARG BUILD_ARCH
ARG BUILD_VERSION
ARG APP_DIR="/app"

LABEL authors="Ryan Snodgrass"

# install git and Python3 environment
RUN apk update \
 && apk add --no-cache bash git python3 jq \
 && python3 -m ensurepip \
 && rm -r /usr/lib/python*/ensurepip \
 && pip3 install --upgrade pip setuptools yq \
 && cd /usr/bin \
 && ln -sf pip3 pip \
 && ln -sf python3 python

RUN git clone https://github.com/rsnodgrass/virtual-ip2sl.git ${APP_DIR} \
 && pip3 install --no-cache-dir -r "${APP_DIR}/requirements.txt" \
 && rm -rf /root/.cache /var/cache

COPY . $APP_DIR

EXPOSE 4998 4999 5000 5001 5002 5003 5004 5005 5006 5007 9131/udp

WORKDIR $APP_DIR
CMD [ "./run.sh" ]
