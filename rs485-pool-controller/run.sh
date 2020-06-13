# /data/options.json is the Hass.io config block saved into the Docker instance
CONFIG_PATH=/data/options.json

# inject the HASS.io configured MQTT credentials via environment variables
MQTT_BROKER_ADDRESS="$(bashio::config 'mqtt_address')"
MQTT_USERNAME="$(bashio::config 'mqtt_username')"
MQTT_PASSWORD="$(bashio::config 'mqtt_password')"

# FIXME:
# - convert HASSIO config.json and apply to nodejs-poolController config style
# - start MQTT bridge as well

# FIXME: run out of server dir

npm start $CONFIG_PATH
