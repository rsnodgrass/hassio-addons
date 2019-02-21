ARG BUILD_FROM=homeassistant/amd64-base:latest
FROM $BUILD_FROM

LABEL authors="Stephen Harris <stephen@homemations.com>"
WORKDIR /app

# Install node and npm
RUN apk update \
 && apk add --no-cache git py-pip python-dev
# && apk add --no-cache --virtual bash \

# Install HomeMation's latest Lutron RadioRA Manager
#
# NOTE: the SmartThings Groovy handlers are also downloaded so that we can
# show them in the HASS add-on configuration view and we ensure that the
# version used matches the version of the Python (in case something changes
# at the same time).
#
RUN git clone https://github.com/homemations/SmartThings/ /homemations

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "/homemations/Lutron RadioRA/lutron/lutronapp.py" ]

# Build arguments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_REF
ARG BUILD_VERSION
