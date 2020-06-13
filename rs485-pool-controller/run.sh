# /data/options.json is the Hass.io config block saved into the Docker instance
CONFIG_PATH=/data/options.json

# inject the HASS.io user configured MQTT credentials via environment variables
MQTT_BROKER_ADDRESS="$(bashio::config 'mqtt_address')"
MQTT_USERNAME="$(bashio::config 'mqtt_username')"
MQTT_PASSWORD="$(bashio::config 'mqtt_password')"

# support RS485-over-IP remote devices using SOcketCAT, e.g. SOCAT_ADDRESS="TCP4:192.168.1.44:80"
SOCAT_OPTIONS="$(bashio::config 'socat')"
if [ ! -z "$SOCAT_OPTIONS" ]
then
    # Examples:
    #   socat -d -d -d -x PTY,raw,ispeed=9600,ospeed=9600,parenb=0,cstopb=1,cs8,link=/dev/ttyRS485-1 tcp:192.168.3.12:10010
    #   socat -d -d pty,link=/dev/ttyS0,raw tcp:192.168.0.10:8899
    echo "Starting socat $SOCAT_OPTIONS"
    socat $SOCAT_OPTIONS &
fi

cd /app
npm start $CONFIG_PATH
