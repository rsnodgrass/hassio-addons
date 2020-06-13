# /data/options.json is the Hass.io config block saved into the Docker instance
CONFIG_PATH=/data/options.json

TARGET="$(bashio::config 'target')"

# FIXME:
# - convert HASSIO config.json and apply to nodejs-poolController config style
# - start MQTT bridge as well

npm start $CONFIG_PATH
