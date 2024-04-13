FROM shawly/keepalived

ARG BUILD_ARCH
ARG BUILD_VERSION

# Install requirements for add-on
RUN apk add --no-cache jq

# Copy root filesystem
COPY rootfs /
RUN chmod a+x /usr/bin/*

ENTRYPOINT [ "/run.sh" ]
