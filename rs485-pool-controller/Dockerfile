# FUTURE: use a build like alpine to make this smaller and faster (one that includes python)
ARG BUILD_FROM=hassioaddons/base:2.3.1
FROM $BUILD_FROM

ARG BUILD_ARCH
ARG BUILD_VERSION

LABEL authors="Ryan Snodgrass"

# install git and Node.js environment
RUN apk update \
 && apk add --no-cache \
            build-base \
            bash \
            git \
            nodejs \
            nodejs-npm \
            python \
            linux-headers

ARG APP_DIR="/nodejs-poolController"

# install latest released version of nodejs-poolController and SmartThings integration
RUN git clone https://github.com/tagyoureit/nodejs-poolController $APP_DIR \
 && git clone https://github.com/bsileo/SmartThings_Pentair $APP_DIR/smartthings \
 && echo '2019-05-12-00' >/dev/null
WORKDIR $APP_DIR

RUN npm install

# /data/options.json is the Hass.io config block saved into the Docker instance
CMD [ "npm", "start", "/data/options.json" ]
