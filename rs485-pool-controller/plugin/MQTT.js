/*
 * MQTT Plugin for NodeJS Pool Controller
 * Copyright (C) 2020 Ryan Snodgrass
 */
var pcpConfig = (function (api) {
    var config = container.settings.getConfig() // FIXME: how is config injected in 6.0?

    var controller_socket = poolController_connect()
    var mqtt = mqtt_setup(config)

    function poolController_connect()_{
        var server_url;
        var server_is_https = false;

        // determine the server URL and whether it is a https secure connection (preferred)
        if (config.poolController.https.enabled) {
            server_is_https = true
            server_url = 'http://localhost:' + bottle.container.settings.get('httpsExpressPort') + '/'
        } else if (config.poolController.http.enabled) {
            server_url = 'http://localhost:' + bottle.container.settings.get('httpExpressPort') + '/'
        } else {

        }

        // listen to events from nodejs-poolController
        var io = container.socketClient
        var socket = io.connect(serverURL, {
            secure: server_is_https,
            reconnect: true,
            rejectUnauthorized: false
        });

        return socket
    }

    function mqtt_setup() {
        // *** IMPORTANT: Ensure you have an environment variable MQTT_BROKER_URL set to your broker
        var broker_url = config.mqtt.broker_ip
        var options = {
            "clientId": "poolController-next-mqtt",
            "username": config.mqtt.username,
            "password": config.mqtt.password
        }

        // allow broker config injection inside containerized deployments (e.g. Docker or Home Assistant add-ons)
        if (process.env.MQTT_BROKER_URL) {
            broker_url = process.env.MQTT_BROKER_URL
            log("MQTT broker url set via ENV variable MQTT_BROKER_URL=" + broker_url)
        }

        // if a MQTT username/password is specified in the environment, use them for connecting to the broker
        // this allows configuration injection inside containerized deployments (e.g. Docker or Home Assistant add-ons)
        if (process.env.MQTT_USERNAME) {
            options['username'] = process.env.MQTT_USERNAME
            options['password'] = process.env.MQTT_PASSWORD
            log("ENV variables MQTT_USERNAME/MQTT_PASSWORD set credentials for user: " + process.env.MQTT_USERNAME)
        }

        var mqtt_broker = require('mqtt')
        var client = mqtt_broker.connect(mqtt_broker_url, options)

        // subscribe to all the relevant MQTT messages upon connect
        client.on('connect', () => { mqtt_subscribe() })

        return client
    }

    function mqtt_subscribe() {
        // FIXME: lowercase only for simplicity (since MQTT topics are case sensitive)
        var prefix = 'pool' // allow override

        var topics = [
            'heater/1/status',
            'heater/1/set',
            
            'pump/1/status',
            'pump/1/set',

            'temperature/pool/status',
            'temperature/spa/status',
            'temperature/air/status',

            'circuit/1/status',
            'circuit/1/set',
            'circuit/2/status',
            'circuit/2/set'
        ]

        for (topics in topics) {
            mqtt.subcribe(prefix + '/' + topic)
        }

        // notify any clients that nodejs-poolController is now connected
        mqtt.publish('pool_controller/connected', 'true')
    }



    socket.on('temperature', function (data) {
        console.log('outputSocketToMQTT: Temperature info as follows: %s', JSON.stringify(data))
        var poolHeatMode = jsonata("temperature.poolHeatMode").evaluate(data)
        var poolSetpoint = jsonata("temperature.poolSetPoint").evaluate(data)
        var spaHeatMode = jsonata("temperature.spaHeatMode").evaluate(data)
        var spaSetpoint = jsonata("temperature.spaSetPoint").evaluate(data)
        var poolTemp = jsonata("temperature.poolTemp").evaluate(data)
        var spaTemp = jsonata("temperature.spaTemp").evaluate(data)
        var airTemp = jsonata("temperature.airTemp").evaluate(data)
        sendMqttHeatStatus(poolHeatMode, poolSetpoint, spaHeatMode, spaSetpoint)
        sendMqttTemp(poolTemp, spaTemp, airTemp)
    })

    // allows logging through all configured loggers for the container
    function log(level, message) {
        logLevel = config.MQTT.level // FIXME: not necessary?
        container.logger[logLevel]('MQTT plugin loaded')
    }

    function init() {
        // intentionally left blank: this plugin has no initialization code
        log('info', 'MQTT plugin loaded') // FIXME: shouldn't the nodejs-poolController do this for *ALL* plugins?
    }

    var module = { init: init };
    init();
    return module;
})(api);
