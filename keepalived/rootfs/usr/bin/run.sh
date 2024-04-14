#!/usr/bin/env bash
# shellcheck shell=dash

set +x

config_get() {
  local config=/data/options.json
  jq --raw-output ".${1}" "$config"
}

# shellcheck disable=2155
{
  export KEEPALIVED_VIRTUAL_IP="$(config_get virtual_ip)"
  export KEEPALIVED_VIRTUAL_MASK="$(config_get virtual_mask)"
  export KEEPALIVED_VRID="$(config_get router_id)"
  export KEEPALIVED_INTERFACE="$(config_get interface)"

  # new options (not in pschmitt version)
  export KEEPALIVED_CHECK_IP="$(config_get check_ip)"
  export KEEPALIVED_CHECK_PORT="$(config_get check_port)" # e.g. 53
  export TZ="$(config_get tz)"

  #export KEEPALIVED_PASSWORD="$(config_get password)"
}

# Run upstream entrypoint
exec /container/tool/run
