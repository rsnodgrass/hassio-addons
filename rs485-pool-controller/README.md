# RS485 Pool Controller (Hass.io Add-On)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This [Hassio](https://www.home-assistant.io/hassio/) add-on allows communication and control for a variety of pool equipment including controllers, pumps, chlorinators, lights, valve controls, etc. which are compatible with the Pentair RS485 communication protocols. This packages up the [nodejs-poolController](https://github.com/tagyoureit/nodejs-poolController) and the [SmartThings Pentair](https://github.com/bsileo/SmartThings_Pentair) integration.

Credit for all the heavy lifting in actually communicating with the pool equipment goes to Russell Goldin, creater of nodejs-poolController, as well as contributors to that project.

### Supported Pool Devices

The following pool devices are known to work with the Pool Controller. For the comprehensive details on the latest supported devices, see the latest release notes for the [nodejs-poolController](https://github.com/tagyoureit/nodejs-poolController).

#### Controllers

* Intermatic PE635RC (plus expansion modules P5043ME, PE25065RC)
* Pentair IntelliTouch
* Pentair EasyTouch
* Pentair IntelliCom II
* Pentair SunTouch

#### Pumps

* Pentair IntelliFlo

#### Chlorinators

* Hayward AquaRite
* Pentair IntelliChlor

#### Lights

* Pentair IntelliBrite

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
3. Follow [nodejs-poolController](https://github.com/tagyoureit/nodejs-poolController) instructions for configuring the RS485 server that interacts with your pool equipment
4. Set the add-on's "tty" config option to the tty path for the RS485 adapter connected to your Hass.io hardware
5. Follow [SmartThings Pentair](https://github.com/bsileo/SmartThings_Pentair) instructions on on how to add the SmartApp and Device Handlers in SmartThings via the [SmartThings Groovy IDE](https://graph.api.smartthings.com/).

#### Step 3 Details: Configuring the Pool Controller

The configuration of the RS485 Pool Controller will take some time and technical skills, see [nodejs-poolController](https://github.com/tagyoureit/nodejs-poolController) for how to use its JSON style configuration.

By default, the ports 9801 is exposed for the service API used for communicating with the RS385 bus, as well as ports 3000 (http) and 3001 (https) for the web UI. For example, http://hassio.local:30000/debug.html.

See the [examples/] folder for some example configurations.

#### Step 5 Details: Setting up SmartThings Integration

See [SmartThings Pentair](https://github.com/bsileo/SmartThings_Pentair) project for how to install the SmartApp and Device Handlers via the [SmartThings Groovy IDE](https://graph.api.smartthings.com/).

Add to your configuration file:

<pre>
   	"outputToSmartThings": 1
   	},
   "outputToSmartThings": {
   	"address": "*",
   	"port": "39500",
   	"logEnabled": 0
   },```
</pre>
