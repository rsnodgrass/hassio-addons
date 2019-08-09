# Run script for use as Hass.io Add-On (passing in config options)
CONFIG_PATH=/data/options.json

#declare -x IP2SL_CONFIG="your-config.yaml"
#IP2SL_CONFIG="$(jq --raw-output '.config-file' $CONFIG_PATH)"

# FIXME: how to convert JSON based Add-on config to YAML?

python3 ip2sl
