ARG BUILD_FROM=hassioaddons/base
FROM $BUILD_FROM

ARG BUILD_ARCH
ARG BUILD_VERSION

# install git and Node.js environment
RUN apk update \
 && apk add --no-cache \
            bash \
            git \
            nodejs \
            nodejs-npm \
            python \
            linux-headers

# add support for RS485-over-IP remote devices
RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

# install latest released versions 
WORKDIR /app
RUN git clone https://github.com/tagyoureit/nodejs-poolController      server \
# && git clone https://github.com/crshersrman/nodejs-poolController-mqtt  mqtt
 && git clone https://github.com/rsnodgrass/nodejs-poolController-mqtt  mqtt

# inject MQTT support as a third-party integration for nodejs-poolController
RUN ln -sf /app/mqtt/src/outputSocketToMQTT.js /app/server/src/integrations

# install any dependencies listed in nodejs-poolController-mqtt's package.json
WORKDIR /app/mqtt
RUN npm install /app/mqtt

# FIXME: next step...
#2. Add the following to the config.json file in the nodejs-poolController folder
# "integrations": { "outputSocketToMQTT": 1 }, "outputSocketToMQTT": { "level": "debug" },

# build the nodejs environment with all the integrations
WORKDIR /app/server
RUN npm install /app/server

COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]