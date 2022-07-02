# /data/options.json is the Hass.io config block saved into the Docker instance
CONFIG_PATH=/data/options.json

# inject the HASS.io user configured MQTT credentials via environment variables
MQTT_BROKER_ADDRESS="$(bashio::config 'mqtt_address')"
MQTT_USERNAME="$(bashio::config 'mqtt_username')"
MQTT_PASSWORD="$(bashio::config 'mqtt_password')"

# support RS485-over-IP to control remote devices using SOcketCAT
SOCAT_OPTIONS="$(bashio::config 'socat')"
if [ ! -z "$SOCAT_OPTIONS" ]
then
    # Examples:
    #   socat -d -d -d -x PTY,raw,ispeed=9600,ospeed=9600,parenb=0,cstopb=1,cs8,link=/dev/ttyRS485-1 tcp:192.168.3.12:10010
    #   socat -d -d pty,link=/dev/ttyS0,raw tcp:192.168.0.10:8899
    echo "Starting socat $SOCAT_OPTIONS"
    socat $SOCAT_OPTIONS &
fi

# make a writable nodejs-poolController.json copy in /config since this can be modified by the web UI
NPM_CONFIG="/config/nodejs-poolController-REVISED.json"
HASS_CONFIG_PATH="$(bashio::config 'config_file')"

# copy the users /config version of pool equipment configuration into the Docker instance
if [ -f "$FILE" ]; then
    cp $HASS_CONFIG_PATH $NPM_CONFIG
else
    echo "FATAL: Missing configuration file $HASS_CONFIG_PATH, aborting!"
    exit
fi

# start the web UI (if it exists)
if [ -f "/app/web" ]; then
    cd /app/web
    npm run start:cached &
fi

cd /app/server
npm start $NPM_CONFIG