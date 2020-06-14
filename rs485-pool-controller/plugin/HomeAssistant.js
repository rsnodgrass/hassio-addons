/*
 * Home Assistant MQTT Auto-Discovery Plugin for NodeJS Pool Controller 6.0+
 *
 * Copyright (C) 2020 Ryan Snodgrass
 */
var plugin = (function (api) {
    var config = container.settings.getConfig() // FIXME: how is config injected in 6.0?

    // FIXME: is there a way to share the MQTT connection with MQTT.js?
    var mqtt = mqtt_setup(config)

    // note, Home Assistant also publishes a format whereby all sensors will be auto-discovered and configured
    // by a running HA instance (no configuration required to setup all the sensors!)
    //
    //   <discovery_prefix>/<component>/[<node_id>/]<object_id>/config
    //   homeassistant/binary_sensor/nodejs-poolController/circuit_1/
    //
    // see https://www.home-assistant.io/docs/mqtt/discovery/
    //
    // FIXME: should probably move this into a SEPARATE integration which is paired with the MQTT integration,
    // as this can get quite complex!
    function publish_hass_discovery_info() {
        mqtt.publish(
            "homeassistant/switch/pool_heater/config",
            '{"name": "Pool Heater", "device_class": "heat", "state_topic": "pool/pool_heater/state", "command_topic": "pool/pool_heater/set"}')
//          '{"name": "Pool Heater", "device_class": "heat", "~": "pool/pool_heater", "state_topic": "~/state", "command_topic": "~/set"}')
    }

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
