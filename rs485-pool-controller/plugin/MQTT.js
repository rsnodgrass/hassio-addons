/*
 * MQTT Plugin for NodeJS Pool Controller
 * Copyright (C) 2020 Ryan Snodgrass
 */
var pcpConfig = (function (api) {
    var config = container.settings.getConfig() // FIXME: how is config injected in 6.0?
    var jsonata = require("jsonata")

    var controller = pool_controller_connect()
    var mqtt = mqtt_connect(config)

    var topic_prefix = 'pool' // allow override from config.MQTT.topic_prefix

    function pool_controller_connect()_{
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

    function mqtt_connect() {
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
        var mqtt_client = mqtt_broker.connect(mqtt_broker_url, options)

        // subscribe to all the relevant MQTT messages upon connect
        mqtt_client.on('connect', () => { mqtt_subscribe() })

        return mqtt_client
    }

    function mqtt_publish(topic, payload) {
        mqtt.publish(topic_prefix + '/' + topic, payload)
    }

    function mqtt_subscribe() {
        // FIXME: lowercase only for simplicity (since MQTT topics are case sensitive)
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
            mqtt.subcribe(topic_prefix + '/' + topic)
        }

        // notify clients that nodejs-poolController is now connected
        mqtt_publish('connected', 'true')
    }

    function example_topic_mapping() {
        var map = {
            "pool": {
                "heatMode": "temperature.poolHeatMode",
                "setPoint": "temperature.poolSetPoint",
            }
        }
    }

    controller.on('temperature', function (data) {
        log('poolController temperature update: %s', JSON.stringify(data))

        // pool
        var pool_temp = {
            "temp": jsonata("temperature.poolTemp").evaluate(data),
        }
        mqtt_publish('pool/temperature/status', JSON.stringify(pool_temp))

        var pool_heater = {
            "mode": jsonata("temperature.poolHeatMode").evaluate(data),
            "setPoint": jsonata("temperature.poolSetPoint").evaluate(data)
        }
        mqtt_publish('pool/heater/status', JSON.stringify(pool_heater))

        // spa
        var spa_temp = {
            "temp": jsonata("temperature.spaTemp").evaluate(data)
        }
        mqtt_publish('spa/temperature/status', JSON.stringify(spa_temp))

        var spa_heater = {
            "mode": jsonata("temperature.spaHeatMode").evaluate(data),
            "setPoint": jsonata("temperature.spaSetPoint").evaluate(data)
        }
        mqtt_publish('spa/heater/status', JSON.stringify(pool_heater))

        // air
        var air_temp = {
            "temp": jsonata("temperature.airTemp").evaluate(data)
        }
        mqtt_publish('air/temperature/status', JSON.stringify(air_temp))
    })

    // allows logging through all configured loggers for the container
    function log(level, message) {
        logLevel = config.MQTT.level // FIXME: not necessary? currently FORCED to this
        container.logger[logLevel]('MQTT: ' + message)
    }

    function init() {
        // intentionally left blank: this plugin has no initialization code
        log('info', 'plugin loaded') // FIXME: shouldn't the nodejs-poolController do this for *ALL* plugins?
    }

    var module = { init: init };
    init();
    return module;
})(api);
