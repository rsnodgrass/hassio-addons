#ARG BUILD_FROM
ARG BUILD_VERSION

FROM shawly/keepalived:latest

ENV LANG C.UTF-8

# install requirements for add-on
RUN apk add --no-cache jq

# copy root filesystem
COPY rootfs /

ENTRYPOINT [ "/usr/bin/run.sh" ]
