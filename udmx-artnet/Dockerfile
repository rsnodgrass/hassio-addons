ARG BUILD_FROM=hassioaddons/base
FROM $BUILD_FROM

ARG BUILD_ARCH
ARG BUILD_VERSION
ARG APP_DIR="/app"

LABEL authors="None"

RUN apk update && apk add --no-cache \
    bash \
    git \
    gcc \
    automake \
    autoconf \
    libtool \
    libusb-dev

# install libartnet
RUN git clone https://github.com/OpenLightingProject/libartnet
RUN cd libartnet \
 && ls -la \
 && autoreconf -fi \
 && ./configure \
 && make \
 && make install

RUN git clone https://github.com/peterdey/udmx-artnet ${APP_DIR} \
 && cd ${APP_DIR} \
 && make

COPY . $APP_DIR

EXPOSE 6454/udp 5568/udp

WORKDIR $APP_DIR
CMD [ "./udmx-artnet", "-v" ]
