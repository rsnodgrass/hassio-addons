ARG BUILD_FROM=hassioaddons/base
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

ARG APP_DIR="/app"
WORKDIR $APP_DIR

RUN npm install

# install latest released versions (FIXME: what is the update strategy for exposing to HASSIO?)
RUN git clone https://github.com/tagyoureit/nodejs-poolController $APP_DIR/server \
 && git clone https://github.com/crsherman/nodejs-poolController-mqtt $APP_DIR/mqtt
# && git clone https://github.com/bsileo/hubitat_poolcontroller $APP_DIR/hubitat

CMD [ "./run.sh" ]