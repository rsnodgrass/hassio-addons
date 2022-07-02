ARG BUILD_FROM=hassioaddons/base
#ARG BUILD_FROM=homeassistant/amd64-base
FROM $BUILD_FROM

ARG BUILD_ARCH
ARG BUILD_VERSION

# expose web UI from nodejs-poolController
EXPOSE 3000 3001 4200 8080
# 4200 = poolController; 8080 = web UI

WORKDIR /app
COPY run.sh /
RUN chmod a+x /run.sh

# install git and Node.js environment
RUN apk update \
 && apk add --no-cache \
            bash \
            git \
            nodejs \
            nodejs-npm \
            python \
            # add support for RS485-over-IP remote devices
            socat \
            # support for when no prebuilt node binaries exist
            musl g++ gcc make \
            linux-headers

# install latest released versions 
# RUN git clone https://github.com/tagyoureit/nodejs-poolController      server \
# && git clone https://github.com/crshersrman/nodejs-poolController-mqtt  mqtt

RUN git clone --single-branch --branch next \
              https://github.com/tagyoureit/nodejs-poolController           server \
 && git clone https://github.com/tagyoureit/nodejs-poolController-webClient web \
 && git clone https://github.com/rstrouse/nodejs-poolController-dashPanel   dashpanel
# && git clone https://github.com/rsnodgrass/nodejs-poolController-mqtt      mqtt

# inject MQTT support as a third-party integration for nodejs-poolController
#RUN ln -sf /app/mqtt/src/outputSocketToMQTT.js /app/server/src/integrations

# install any dependencies listed in nodejs-poolController-mqtt's package.json
WORKDIR /app/mqtt
RUN npm install .

# ...install UI
WORKDIR /app/web
RUN npm install .

# ...and build the nodejs-poolController with the injected integrations
WORKDIR /app/server
RUN npm install .

CMD [ "/run.sh" ]
