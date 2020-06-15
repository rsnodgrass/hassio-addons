/*
 * Home Assistant MQTT Auto-Discovery Plugin for NodeJS Pool Controller 6.0+
 *
 * This advertises the available MQTT topics/messages to Home Assistant (HA) so that HA can automatically
 * discover all the sensors, switches, etc. without custom configuration. Technically this could be used
 * for any digital/virtual pool controller that supports the pool MQTT message structure, but is initially
 * intended for nodejs-poolController.
 * 
 * FIXME: Perhaps the pattern is to provide TWO+ discover mechanisms for MQTT topics, one is HA and the
 * other is Homie style?  Surely there could be an automatic mapping between the two.
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

/*
# sensor_type [ description, unit, icon ]
SENSOR_TYPES = {
    "air_temp": ["Air Temperature", TEMP_UNITS, "mdi:thermometer"],
    "pool_temp": ["Pool Temperature", TEMP_UNITS, "mdi:oil-temperature"],
    "spa_temp": ["Spa Temperature", TEMP_UNITS, "mdi:oil-temperature"],
    "pool_chlorinator": ["Pool Chlorinator", PERCENT_UNITS, "mdi:gauge"],
    "spa_chlorinator": ["Spa Chlorinator", PERCENT_UNITS, "mdi:gauge"],
    "salt_level": ["Salt Level", SALT_UNITS, "mdi:gauge"],
    "pump_speed": ["Pump Speed", PERCENT_UNITS, "mdi:speedometer"],
    "pump_power": ["Pump Power", WATT_UNITS, "mdi:gauge"],
    "status": ["Status", NO_UNITS, "mdi:alert"],
}
*/

/*
Or alternative from https://github.com/bwoodworth/hassio-addons/blob/master/pentair-screenlogic/configuration-entries.yaml

# You can create more switches for other circuits in you pool controller (lights, jets, cleaner, etc.)  
# Just use the same convention and change the circuit ID
switch:
  - platform: mqtt
    name: pentair_pool
    command_topic: pentair/circuit/505/command
    state_topic: pentair/circuit/505/state

  - platform: mqtt
    name: pentair_spa
    command_topic: pentair/circuit/500/command
    state_topic: pentair/circuit/500/state

*/


/* MQTT message structure used by hassio-screenlogic-addon 
   FIXME: do we mimic?
   https://github.com/krk628/hassio-screenlogic-addon/blob/master/send_state_to_ha.js

console.log('/pentair/pooltemp/state,' + status.currentTemp[0]);
    console.log('/pentair/spatemp/state,' + status.currentTemp[1]);
    console.log('/pentair/airtemp/state,' + status.airTemp);
    console.log('/pentair/saltppm/state,' + status.saltPPM);
    console.log('/pentair/ph/state,' + status.pH);
    console.log('/pentair/saturation/state,' + status.saturation);
    if (status.isSpaActive()) {
        console.log('/pentair/spa/state,ON');
    } else {
        console.log('/pentair/spa/state,OFF');
    }
    if (status.isPoolActive()) {
        console.log('/pentair/pool/state,ON');
    } else {
        console.log('/pentair/pool/state,OFF');
    }
  }).on('chemicalData', function(chemData) {
    console.log('/pentair/calcium/state,' + chemData.calcium);
    console.log('/pentair/cyanuricacid/state,' + chemData.cyanuricAcid);
    console.log('/pentair/alkalinity/state,' + chemData.alkalinity);


switch:
  - platform: mqtt
    name: pentair_pool
    command_topic: /pentair/pool/command
    state_topic: /pentair/pool/state

  - platform: mqtt
    name: pentair_spa
    command_topic: /pentair/spa/command
    state_topic: /pentair/spa/state

sensor:

  - platform: mqtt
    name: pentair_pooltemp
    state_topic: /pentair/pooltemp/state

  - platform: mqtt
    name: pentair_spatemp
    state_topic: /pentair/spatemp/state

  - platform: mqtt
    name: pentair_airtemp
    state_topic: /pentair/airtemp/state

  - platform: mqtt
    name: pentair_alkalinity
    state_topic: /pentair/alkalinity/state

  - platform: mqtt
    name: pentair_calcium
    state_topic: /pentair/calcium/state

  - platform: mqtt
    name: pentair_cyanuricacid
    state_topic: /pentair/cyanuricacid/state

  - platform: mqtt
    name: pentair_ph
    state_topic: /pentair/ph/state

  - platform: mqtt
    name: pentair_saltppm
    state_topic: /pentair/saltppm/state

  - platform: mqtt
    name: pentair_saturation
    state_topic: /pentair/saturation/state


*/