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
if [ -f /ha_config/keepalived.conf ]; then
    echo "Custom config /etc/keepalived/keepalived.conf used"
    cp /ha_config/keepalive.conf /etc/keepalived

    # enable config for keepalived to use the custom config in /etc/keepalived/keepalived.conf
    export_config KEEPALIVED_CUSTOM_CONFIG true
fi

# call shawly/docker-keepalived entrypoint
exec /init
