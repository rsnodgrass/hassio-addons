# RS485 Pool Controller (Hass.io Add-On)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# DOES NOT WORK YET

[Hass.io](https://www.home-assistant.io/hassio/) add-on to enable communication and control for a variety of pool devices including controllers, pumps, chlorinators, lights, and other controls compatible with the Pentair RS485 serial bus communication protocol. This packages up  [nodejs-poolController](https://github.com/bsileo/hubitat_poolcontroller) and [poolController-MQTT](https://github.com/crsherman/nodejs-poolController-mqtt) into a Hass.io compatible add-one package. Credit for all the heavy lifting in actually communicating with the pool equipment goes to Russell Goldin, creater of nodejs-poolController, as well as contributors to the project's success including Brad Sileo, Jason Young, Michael Russe, Michael Usner and many others.

#### TODO

* figure out the HASS.IO update strategy to keep the dependencies up-to-date when new versions are released (without having to manually release new versions of the HASS.IO add-on)
* also possibly add [Hubitat/SmartThings Pool Controller](https://github.com/bsileo/hubitat_poolcontroller) to the Docker image?

### Supported Pool Devices

For comprehensive details on the latest supported devices, see the release notes for the [nodejs-poolController](https://github.com/tagyoureit/nodejs-poolController).

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

#### Salt Chlorinators

| Hardware             | Models | Notes |
| -------------------- | ------ | ----- |
| [Hayward/Goldline AquaRite](https://www.amazon.com/Hayward-AQR3-Electronic-Chlorination-000-Gallon/dp/B07ST63P4W?tag=rynoshark-20) |        |       |
| Pentair IntelliChlor |        |       |

#### Lights

| Hardware             | Models | Notes |
| -------------------- | ------ | ----- |
| Pentair IntelliBrite |        |       |

### Required Hardware

* RS485 serial adapter connected to the hardware running Hass.io, examples: 
  - [JBtek USB to RS485 adapter](https://amzn.com/B00NKAJGZM?tag=carreramfi-20)
  - direct wired to device's GPIO pins (e.g. on Raspberry Pi)
* RS485 wiring to each device

NOTE: Remote-over-IP RS485 devices are not yet supported.

## Hass.io Setup

Setting up the RS485 Pool Controller is not for the faint of heart, as quite a few configuration steps are required by the underlying technology determining how it communicates with your pool equipment.

1. In the Hass.io "Add-On Store" on your Home Assistant, add the repository URL:
<pre>
     https://github.com/rsnodgrass/hassio-addons
</pre>
2. Find "RS485 Pool Controller" in the list of add-ons and click Install
3. Follow [nodejs-poolController](https://github.com/tagyoureit/nodejs-poolController) instructions for configuring the RS485 server that interacts with your pool equipment
4. Set the add-on's "tty" config option to the tty path for the RS485 adapter connected to your Hass.io hardware

#### Step 3 Details: Configuring the Pool Controller

The configuration of the RS485 Pool Controller will take some time and technical skills, see [nodejs-poolController](https://github.com/tagyoureit/nodejs-poolController) for how to configure. By default, the port 9801 is exposed for the service API used for communicating with the RS385 bus, as well as ports 3000 (http) and 3001 (https) for the web UI. For example, http://hassio.local:30000/debug.html.

In the "Config" JSON text box in the RS485 Pool Controller add-on page, copy and paste the JSON configuration for
your pool equipment. There is no input validation as the complex configuration is directly consumed by nodejs-poolController, thus you will have to look at the log file upon startup to debug and problems. See the [examples/] folder for several example configurations.


# See Also

* [Home Assistant Community Support](https://community.home-assistant.io/t/new-addon-pentair-screenlogic/162332/83)
* [SmartThings Community Support](https://community.smartthings.com/t/intermatic-pe653-pool-control-system/936)
