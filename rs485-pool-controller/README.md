# RS485 Pool Controller (Hass.io Add-On)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This [Hassio](https://www.home-assistant.io/hassio/) add-on allows communucation with and control of a variety of pool equipment such as pumps, chlorinators, valve controls, etc that are compatible with the Pentair RS485 communication protocols by packaging up the [nodejs-poolController](https://github.com/tagyoureit/nodejs-poolController) and the [SmartThings Pentair](https://github.com/bsileo/SmartThings_Pentair) integration. Note that this requires Home Assistant 0.87 or later as this add-on relies on native SmartThings integration (rather than the added complexity of a MQTT bridge).

Credit goes to Russell Goldin, creater of nodejs-poolController, and contributors to that project for all the heavy lifting in actually communicating with the pool equipment.

### Supported Pool Devices

The following pool devices are known to work with the Pool Controller. For the comprehensive details on the latest supported devices, see the latest release notes for the [nodejs-poolController](https://github.com/tagyoureit/nodejs-poolController).

#### Controllers

* Intermatic PE635RC 
* Intermatic Expansion Modules (P5043ME, PE25065RC)
* Pentair IntelliTouch
* Pentair EasyTouch
* Pentair IntelliCom II
* Pentair SunTouch

#### Pumps

* Pentair IntelliFlo

#### Chlorinators

* Hayward Aqua-Rite
* Pentair IntelliChlor

### Required Hardware

* RS485 serial adapter connected to the hardware running Hass.io, examples: 
- [JBtek USB to RS232 adapter](https://www.amazon.com/gp/product/B00NKAJGZM)
- direct wired to device's GPIO pins (e.g. on Raspberry Pi)
* RS485 cabling to each device

### Hass.io Setup

1. In the Hass.io "Add-On Store" on your Home Assistant, add the repository URL:
<pre>
     https://github.com/rsnodgrass/hassio-addons
</pre>
2. Find the "RS485 Pool Controller" in the add-ons and click Install
3. Follow [nodejs-poolController](https://github.com/tagyoureit/nodejs-poolController) on how to add the SmartApp and Device Handler in SmartThings. You can manage the SmartApp and Device Handler via the [SmartThings Groovy IDE](https://graph.api.smartthings.com/).
4. Set the add-on's "tty" config option to the tty path for the RS485 adapter connected to your Hass.io hardware

### Configuration

TBD

Uses a config.json for defining your setup.

See examples

### Debugging

http://_your_machine_name_:3000/debug.html

