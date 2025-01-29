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
#    export_config KEEPALIVED_INTERFACE
#    export_config KEEPALIVED_VIRTUAL_IP
#    export_config KEEPALIVED_VIRTUAL_MASK
#    export_config KEEPALIVED_VRID
#    export_config KEEPALIVED_CHECK_IP
#    export_config KEEPALIVED_CHECK_PORT
    export_config TZ
}

# copy from Home Assistant /config directory any keepalived.conf foun
CONFIG_SRC=/homeassistant_config/keepalived.conf
CONFIG_DEST=/etc/keepalived/keepalived.conf
if [ -f $CONFIG_SRC ]; then
    echo "[INFO] Copying $CONFIG_SRC to $CONFIG_DEST"
    chmod 644 $CONFIG_DEST
    cp $CONFIG_SRC $CONFIG_DEST

    # instruct keepalived to use the custom config in /etc/keepalived/keepalived.conf
    export KEEPALIVED_CUSTOM_CONFIG=true

    # call shawly/docker-keepalived entrypoint
    exec /init
else
    echo "[FATAL] Missing Home Assistant /config/keepalived.conf file, cannot start Keepalived!"
fi
