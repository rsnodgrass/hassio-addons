# /data/options.json is the Hass.io config block saved into the Docker instance
CONFIG_PATH=/data/options.json

# inject the HASS.io user configured MQTT credentials via environment variables
MQTT_BROKER_ADDRESS="$(bashio::config 'mqtt_address')"
MQTT_USERNAME="$(bashio::config 'mqtt_username')"
MQTT_PASSWORD="$(bashio::config 'mqtt_password')"

# FIXME:
# - convert HASSIO config.json and apply to nodejs-poolController config style
# - start MQTT bridge as well

# FIXME: run out of server dir

# support RS485-over-IP remote devices using SOcketCAT, e.g. SOCAT_ADDRESS="TCP4:192.168.1.44:80"
SOCAT_ADDRESS="$(bashio::config 'socat_address')"
if [ ! -z "$SOCAT_OPTIONS" ]
then
    socat -d -d - $SOCAT_ADDRESS
      echo "\$var is NOT empty"
fi
socat


npm start $CONFIG_PATH
