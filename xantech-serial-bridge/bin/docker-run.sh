#!/bin/bash

if [ "$SERIAL_BRIDGE_TTY" != "" ]; then
  EXTRA_OPTIONS="--env SERIAL_BRIDGE_TTY=\"$SERIAL_BRIDGE_TTY\" --device=\"$SERIAL_BRIDGE_TTY\""
fi

CMD="docker run --privileged -t -i $EXTRA_OPTIONS RESTful-serial-bridge"
echo "Executing: $CMD"
$CMD
