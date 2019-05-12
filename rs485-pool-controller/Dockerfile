# FUTURE: use a build like alpine to make this smaller and faster (one that includes python)
ARG BUILD_FROM=hassioaddons/base:2.3.1
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
 && rm -rf /root/.cache /var/cache

# install latest released version of nodejs-poolController
# https://github.com/tagyoureit/nodejs-poolController

ARG APP_DIR="/nodejs-poolController"
RUN git clone https://github.com/tagyoureit/nodejs-poolController $APP_DIR \
 && echo '2019-05-11-00' >/dev/null

# install the SmartThings integration
RUN git clone https://github.com/bsileo/SmartThings_Pentair $APP_DIR/smartthings-pentair

WORKDIR $APP_DIR
CMD [ "./docker-run.sh" ]
