# RS485 Pool Controller (Hass.io Add-On)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[Home Assistant](https://home-assistant.io) add-on to enable communication and control for a variety of pool devices including controllers, pumps, chlorinators, lights, valve controls, etc. which are compatible with the Pentair RS485 communication protocol. This packages up  [nodejs-poolController](https://github.com/bsileo/hubitat_poolcontroller) and the [nodejs-poolController MQTT integration](https://github.com/crsherman/nodejs-poolController-mqtt) into a [Hass.io](https://www.home-assistant.io/hassio/) compatible add-on package (using Docker). Credit for all the heavy lifting in actually communicating with the pool equipment goes to Russell Goldin, creater of nodejs-poolController, as well as contributors to the project's success including Brad Sileo, Jason Young, Michael Russe, Michael Usner and many others.

## Required Hardware

* RS485 serial adapter connected from Hass.io instance hardware to each controlled pool equipment, for example:
  - [JBtek USB to RS485 adapter](https://amzn.com/B00NKAJGZM?tag=carreramfi-20)
  - direct wired to device's GPIO pins (e.g. on Raspberry Pi)

NOTE: Remote-over-IP RS485 devices are not yet supported, but the plan is to add using socat (SOcketCAT). An alpha implementation of socat integration has been added, but not tested.

### Supported Pool Equipment

For comprehensive details on the latest supported devices, see the [nodejs-poolController](https://github.com/tagyoureit/nodejs-poolController) wiki for details on currently supported equipment.

#### Controllers

| Hardware                                                                                                                 | Models | Notes                                                             |
| ------------------------------------------------------------------------------------------------------------------------ | ------ | ----------------------------------------------------------------- |
| [Pentair IntelliTouch](https://www.pentair.com/en/products/pool-spa-equipment/pool-automation/intellitouch_systems.html) |        |                                                                   |
| Pentair EasyTouch                                                                                                        |        |                                                                   |
| Pentair IntelliCom II                                                                                                    |        |                                                                   |
| Pentair SunTouch                                                                                                         |        |                                                                   |
| [Intermatic PE653RC](https://www.intermatic.com/en/pool-and-spa/electronic-controls/pe653rc)                             |        | Unknown if supported; (plus expansion modules P5043ME, PE25065RC) |

#### Pumps

| Hardware           | Models | Notes |
| ------------------ | ------ | ----- |
| Pentair IntelliFlo |        |       |

#### Chlorinators

| Hardware             | Models | Notes |
| -------------------- | ------ | ----- |
| Hayward AquaRite     |        |       |
| Pentair IntelliChlor |        |       |

#### Lights

| Hardware             | Models | Notes |
| -------------------- | ------ | ----- |
| Pentair IntelliBrite |        |       |

## Hass.io Add-on Installation

Setting up the RS485 Pool Controller is not for the faint of heart, as quite a few configuration steps are required by the underlying technology determining how it communicates with your pool equipment.

1. In the Hass.io "Add-On Store" on your Home Assistant, add the repository URL:
<pre>
     https://github.com/rsnodgrass/hassio-addons
</pre>
2. Find "RS485 Pool Controller" in the list of add-ons and click Install
3. Set the add-on's "tty" config option to the tty path for the RS485 adapter connected to your Hass.io hardware.  **NOTE: If you are using a localhost tty other than /dev/ttyUSB0 or /dev/ttyAMA0 this may not work as the TTY hardware devices are not exposed into the Docker container by default.**

Example HASS.io configuration:

```json
"mqtt_broker": "http://192.168.1.8:1883",
"mqtt_username": "your-mqtt-username",
"mqtt_password": "your-mqtt-password"
```

## Configuring the Pool Controller

The configuration of the RS485 Pool Controller requires some technical skills, see [nodejs-poolController](https://github.com/tagyoureit/nodejs-poolController) for details how to configure. 

**Important: Instead of the standard 'config.json' file, the Pool Controller configuration is stored in `nodejs-poolController.json` located at the root of Home Assistant's config directory (e.g. `/config`).** There is no input validation as the complex configuration is directly consumed by nodejs-poolController, thus you will have to look at the log file upon startup to debug and problems. See the [examples/] folder for several example configs.

**MAKE SURE YOU USE ONE OF THE EXAMPLE AS A BASELINE TO ENSURE MQTT SUPPORT IS ENABLED.** The following **MUST** exist in your nodejs-poolController.json for the Home Assistant MQTT integration to work:

```json
    "integrations": {
        "outputSocketToMQTT": 1
    },
    "outputSocketToMQTT": {
        "level": "debug"
    },
```

**FIXME**: The user needs access to the Docker image's nodejs-poolController.json to get values such as the RPM values for VF pumps which MUST be set via the web UI.

#### Web UI

By default, the nodejs-poolController web UI is exposed on ports 3000 (http) and 3001 (https). These are exposed as Home Assistant ingress ports, so no need for any router configuration to access the web UI. For example, http://hassio.local:3000/debug.html.

## Home Assistant Configuration

### Adding Sensor/Switches

Ideally, sensors/switches would automatically be created in Home Assistant using either a HACS integration, or via Home Assistant integrated discovery, or via configured sensors from nodejs-poolController.  However, currently this requires manual configuration.yaml additions.

Examples:

```yaml
sensor:
  - platform: mqtt
    name: "Pool Temperature"
    state_topic: "home/pool/temperature"

  - platform: mqtt
    name: "Salt Level"
    state_topic: "home/swg/level"

switch:
  - platform: mqtt
    name: "Pool Pump"
    icon: mdi:fan
    command_topic: "home/pump/set"
    state_topic: "home/pump"
    payload_on: "on"
    payload_off: "off"

  - platform: mqtt
    name: "Salt Chlorinator"
    command_topic: "home/swg/set"
    state_topic: "home/swg"
    payload_on: "on"
    payload_off: "off"
```
 
### Lovelace UI

Examples:

```yaml
entities:
```

## Advanced 


### Node-RED Recipes

In addition to control via the Home Assistant user interface and its built in automation mechanisms, it is possible to use [Node-RED](https://nodered.org/). The following are several Node-RED recipes for typical pool automation scenarios. **(NOT YET ADDED)**

### Socat

**FIXME** From nodejs-poolController.json docs, requires special config. This is advanced and not yet supported.

```json
        "network": {
            "rs485Port": "/dev/ttyUSB0",
            "netConnect": 1,
            "netHost": "192.168.20.222",
            "netPort": 9801,
            "inactivityRetry": 10
        }
```

To connect to native rs485 traffic for connectivity/debugging using SOCAT 1. netConnect: 1 to enable or 0 to disable. If you enable this option, it will NOT connect to the local RS485 adapter 1. netHost: Name/IP of your remote computer. EG raspberrypi 1. "netPort":: 9801 is a standard port


## Known Issues

### Planned Features

* add support for RS485-over-IP to remote RS485 devices using [SOcketCAT](https://medium.com/@copyconstruct/socat-29453e9fc8a6)
* support for [nodejs-poolController 6.0](https://github.com/tagyoureit/nodejs-poolController/tree/next) and the new [standalone 6.0 web UI](https://github.com/tagyoureit/nodejs-poolController-webClient)

### No Plans to Implement

* possibly add [Hubitat/SmartThings Pool Controller](https://github.com/bsileo/hubitat_poolcontroller) to the Docker image?

## Support

* [nodejs-poolController support chat](https://gitter.im/nodejs-poolController/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
* https://community.smartthings.com/t/intermatic-pe653-pool-control-system/936

### See Also

* [nodejs-poolController](https://github.com/tagyoureit/nodejs-poolController): interface for communicating via RS485 to a variety of pool equipment
