#!/bin/bash

# Run script for use as Hass.io Add-On (passing in config options)
HASS_CONFIG_PATH=/data/options.json

echo "Home Assistant config:"
cat $HASS_CONFIG_PATH

# convert Hass.io JSON based config to yaml
declare -x IP2SL_CONFIG=/data/options.yaml
yq -y . $HASS_CONFIG_PATH > $IP2SL_CONFIG
echo ""
echo "YAML converted config:"
cat $IP2SL_CONFIG

python3 ip2sl
