# FUTURE: use a build like alpine to make this smaller and faster (one that includes python)
ARG BUILD_FROM=hassioaddons/base:2.3.1
FROM $BUILD_FROM

ARG BUILD_ARCH
ARG BUILD_VERSION

LABEL authors="Ryan Snodgrass"

# install git and Node.js environment
RUN apk update \
 && apk add --no-cache bash git nodejs nodejs-npm

# install latest released version of nodejs-poolController and SmartThings integration
ARG APP_DIR="/nodejs-poolController"
RUN git clone https://github.com/tagyoureit/nodejs-poolController $APP_DIR \
 && git clone https://github.com/bsileo/SmartThings_Pentair $APP_DIR/smartthings \
 && echo '2019-05-11-00' >/dev/null

# install the SmartThings integration
RUN npm install

WORKDIR $APP_DIR
CMD [ "npm", "start" ]
