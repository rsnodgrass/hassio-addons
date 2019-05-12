# FUTURE: use a build like alpine to make this smaller and faster (one that includes python)
ARG BUILD_FROM=hassioaddons/base:2.3.1
FROM $BUILD_FROM

ARG BUILD_ARCH
ARG BUILD_VERSION

LABEL authors="Ryan Snodgrass"

# install git and Python3 environment
RUN apk update \
 && apk add --no-cache bash git python3 \
 && python3 -m ensurepip \
 && rm -r /usr/lib/python*/ensurepip \
 && pip3 install --upgrade pip setuptools \
 && cd /usr/bin \
 && ln -sf pip3 pip \
 && ln -sf python3 python \
 && rm -rf /root/.cache /var/cache

# install HomeMation's latest Lutron RadioRA Classic Bridge
ARG HOMEMATIONS_DIR="/homemations/Lutron RadioRA Classic/Bridge"
#RUN git clone https://github.com/homemations/SmartThings/ /homemations
RUN git clone https://github.com/rsnodgrass/SmartThings/ /homemations \
 && pip install --no-cache-dir -r "${HOMEMATIONS_DIR}/requirements.txt" \
 && echo '2019-02-26-00' >/dev/null

# overwrite the default db.sqlite with our defaults (until better config option exists)
#COPY data/db.sqlite "${HOMEMATIONS_DIR}/lutron"
#COPY data/db.sqlite "${HOMEMATIONS_DIR}/"

EXPOSE 8333

WORKDIR $HOMEMATIONS_DIR
#CMD [ "python3", "radiora-classic-bridge.py" ]
CMD [ "./docker-run.sh" ]
