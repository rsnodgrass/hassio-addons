# FUTURE: use a build like alpine to make this smaller and faster (one that includes python)
ARG BUILD_FROM=hassioaddons/base:2.3.1
FROM $BUILD_FROM

ARG BUILD_ARCH
ARG BUILD_VERSION

LABEL authors="Ryan Snodgrass"

# install git and nodeJS environment
RUN apk update \
 && apk add --no-cache bash git npm \
 && npm install

# install latest released version of nodejs-poolController
# https://github.com/tagyoureit/nodejs-poolController

ARG APP_DIR="/nodejs-poolController"
RUN git clone https://github.com/tagyoureit/nodejs-poolController $APP_DIR \
 && echo '2019-05-11-00' >/dev/null

# install the SmartThings integration
RUN git clone https://github.com/bsileo/SmartThings_Pentair $APP_DIR/smartthings-pentair

EXPOSE 9801

WORKDIR $APP_DIR
CMD [ "node", "server.js" ]
