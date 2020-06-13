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

WORKDIR /app

# install latest released versions (FIXME: what is the update strategy for exposing to HASSIO?)
RUN git clone https://github.com/tagyoureit/nodejs-poolController      server \
 && git clone https://github.com/crsherman/nodejs-poolController-mqtt  mqtt
# && git clone https://github.com/bsileo/hubitat_poolcontroller        hubitat

# modify the package.json to add support for nodejs-poolController-mqtt

#1. Add the following to the package.json file in the nodejs-poolController folder
# "jsonata": "^1.5.3", "mqtt": "^2.17.0",
#2. Add the following to the config.json file in the nodejs-poolController folder
# "integrations": { "outputSocketToMQTT": 1 }, "outputSocketToMQTT": { "level": "debug" },
#3. Modify outputSocketToMQTT.js line 42 to specify the IP address of YOUR MQTT server on your network.
#4. Add the outputSocketToMQTT.js file to the nodejs-poolController/src/integrations folder on your rapsberry pi
#5. Run npm install in the nodejs-poolController folder where package.json exists

RUN npm install /app/server

COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]