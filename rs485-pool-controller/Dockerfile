ARG BUILD_FROM=hassioaddons/base
FROM $BUILD_FROM

ARG BUILD_ARCH
ARG BUILD_VERSION

LABEL authors="Ryan Snodgrass"

# install git and Node.js environment
RUN apk update \
 && apk add --no-cache \
            bash \
            git \
            nodejs \
            nodejs-npm \
            python \
            linux-headers

RUN npm install

WORKDIR /app

# install latest released versions (FIXME: what is the update strategy for exposing to HASSIO?)
RUN git clone https://github.com/tagyoureit/nodejs-poolController      /app/server \
 && git clone https://github.com/crsherman/nodejs-poolController-mqtt  /app/mqtt
# && git clone https://github.com/bsileo/hubitat_poolcontroller        /app/hubitat

COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]