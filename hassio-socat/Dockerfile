ARG BUILD_FROM=hassioaddons/base
FROM $BUILD_FROM
# alternative: alpine/socat

LABEL authors="rsnodgrass@"

RUN apk add --no-cache socat jq bash

COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "./run.sh" ]
