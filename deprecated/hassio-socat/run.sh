#!/usr/bin/env bashio

CONFIG_PATH=/data/options.json

LOGGING=$(bashio::info 'hassio.info.logging' '.logging')

bashio::log.debug "Setup socat configuration"

if [ "${LOGGING}" == "debug" ]; then
    # -d... : The most amount of logging
    # -lu   : Timestamp of error messages to microsecond resolution
    # -v    : Writes the transferred data not only to their target streams, but also to stderr
    LOG_LEVEL_FLAGS="-d -d -d -d -lu -v"
elif [ "${LOGGING}" == "info" ]; then
    LOG_LEVEL_FLAGS="-d -d -d"
else
    LOG_LEVEL_FLAGS="-d"
fi


bashio::log.warning "socat is not yet implemented"

PTY="$(jq --raw-output '.pty' $CONFIG_PATH)


# iterate through each configured post and create
# socat pty,link=$HOME/dev/ttyV0,waitslave tcp:remoteip:remoteport    # ,fork
# WAIT_PIDS+=($!)

# Wait and hold Add-on running while any socat processes are still running
#wait "${WAIT_PIDS[@]}"

# FIXME: how to handle shutdown gracefully?


