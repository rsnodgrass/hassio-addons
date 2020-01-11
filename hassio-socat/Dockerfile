ARG BUILD_FROM=hassioaddons/base
FROM $BUILD_FROM
# alpine/socat

ARG BUILD_ARCH
ARG BUILD_VERSION

LABEL authors="rsnodgrass@"

RUN apk add --update socat bash && \
    rm -rf /var/cache/apk/*

ENV APP_DIR=/app
ADD . $APP_DIR
WORKDIR $APP_DIR

CMD [ "./run.sh" ]
