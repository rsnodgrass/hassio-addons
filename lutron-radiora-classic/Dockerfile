# FUTURE: use a build like alpine to make this smaller and faster (one that includes python)
ARG BUILD_FROM=hassioaddons/base:2.3.1
FROM ${BUILD_FROM}

ARG BUILD_ARCH
ARG BUILD_VERSION

LABEL authors="Ryan"
WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt

# install git and the require python environment
RUN apk update \
 && apk add --no-cache git python-dev py-pip
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Install HomeMation's latest Lutron RadioRA Manager
#
# NOTE: the SmartThings Groovy handlers are also downloaded so that one
# day we can show them in the HASS add-on configuration view and we ensure
# that the version used matches the version of the Python (in case something
# changes at the same time).
#
#RUN git clone https://github.com/homemations/SmartThings/ /homemations
RUN git clone https://github.com/rsnodgrass/SmartThings/ /homemations

ENTRYPOINT [ "python" ]
CMD [ "/homemations/Lutron RadioRA/lutron/lutronapp.py" ]
