#ARG BUILD_FROM
ARG BUILD_VERSION

FROM shawly/keepalived:latest

ENV LANG C.UTF-8

# install requirements for add-on
RUN apk add --no-cache jq

# copy root filesystem
COPY rootfs /

# call shawly/docker-keepalived entry point
ENTRYPOINT [ "/init" ]
