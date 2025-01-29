#!/usr/bin/env ash
# shellcheck shell=dash

set -x

cat /data/options.json

config_get() {
  local config=/data/options.json
  jq --raw-output ".${1}" "$config"
}

export_config() {
  export $1="$(config_get ${1})"
}

# shellcheck disable=2155
{
    export_config KEEPALIVED_INTERFACE

    export_config KEEPALIVED_VIRTUAL_IP
    export_config KEEPALIVED_VIRTUAL_MASK
    export_config KEEPALIVED_VRID

    export_config KEEPALIVED_CHECK_IP
    export_config KEEPALIVED_CHECK_PORT

    export_config TZ
}


# copy from Home Assistant /config directory any keepalived.conf foun
CONFIG_SRC=/homeassistant_config/keepalived.conf
if [ -f $CONFIG_SRC ]; then
    echo "Copying $CONFIG_SRC to /etc/keepalived/keepalived.conf"
    cp $CONFIG_SRC /etc/keepalived

    # instruct keepalived to use the custom config in /etc/keepalived/keepalived.conf
    export_config KEEPALIVED_CUSTOM_CONFIG true
else
    echo "Missing Home Assistant /config/keepalived.conf file, cannot start keepalived!"
fi

# FIXME: fail to start if missing CONFIG_SRC !!!

# call shawly/docker-keepalived entrypoint
exec /init
