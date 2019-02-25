# FUTURE: use a build like alpine to make this smaller and faster (one that includes python)
ARG BUILD_FROM=hassioaddons/base:2.3.1
FROM $BUILD_FROM

ARG BUILD_ARCH
ARG BUILD_VERSION

LABEL authors="Ryan"

# install git and the require python environment
RUN apk update \
 && apk add --no-cache bash git python-dev py-pip \
 && pip install --upgrade pip

# install HomeMation's latest Lutron RadioRA Classic Bridge
#
# NOTE: the SmartThings Groovy handlers are also downloaded so that one
# day we can show them in the HASS add-on configuration view and we ensure
# that the version used matches the version of the Python (in case something
# changes at the same time).
#
ARG HOMEMATIONS_DIR="/homemations/Lutron RadioRA Classic/Bridge"
#RUN git clone https://github.com/homemations/SmartThings/ /homemations
RUN git clone https://github.com/rsnodgrass/SmartThings/ /homemations \
 && pip install --no-cache-dir -r "${HOMEMATIONS_DIR}/requirements.txt" \
 && echo '2019-02-24-00' >/dev/null

# Overwrite the default db.sqlite with basic Zone file (until better config option exists)
#COPY data/db.sqlite "${HOMEMATIONS_DIR}/lutron"
#COPY data/db.sqlite "${HOMEMATIONS_DIR}/"

WORKDIR $HOMEMATIONS_DIR
ENTRYPOINT ["./run.sh"]
