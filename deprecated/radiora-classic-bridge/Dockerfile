ARG BUILD_FROM=hassioaddons/base
FROM $BUILD_FROM

ARG BUILD_ARCH
ARG BUILD_VERSION

LABEL authors="Homemations"

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

# install Homemation's latest Lutron RadioRA Classic Bridge
ARG APP_DIR="/homemations/Lutron RadioRA Classic/Bridge"

RUN git clone https://github.com/rsnodgrass/Homemations-SmartThings/ /homemations \
 && pip install --no-cache-dir -r "${APP_DIR}/requirements.txt"

# FUTURE: overwrite the default db.sqlite with our defaults (until better config option exists)
#COPY data/db.sqlite "${APP_DIR}/lutron"

EXPOSE 8333

WORKDIR $APP_DIR
CMD [ "./run.sh" ]
