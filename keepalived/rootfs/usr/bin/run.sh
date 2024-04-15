#!/usr/bin/env bash
# shellcheck shell=dash

set -x

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

#    export KEEPALIVED_VIRTUAL_IP="$(config_get virtual_ip)"
#    export KEEPALIVED_VIRTUAL_MASK="$(config_get virtual_mask)"
#    export KEEPALIVED_VRID="$(config_get router_id)"
#    export KEEPALIVED_INTERFACE="$(config_get interface)"
#    export KEEPALIVED_CHECK_IP="$(config_get check_ip)"
#    export KEEPALIVED_CHECK_PORT="$(config_get check_port)" # e.g. 53
#    export TZ="$(config_get tz)"

    #export KEEPALIVED_PASSWORD="$(config_get password)"
}

# run upstream entrypoint
exec /container/tool/run
