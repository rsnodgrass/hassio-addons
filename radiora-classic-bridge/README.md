# RadioRA Classic Smart Bridge (Hass.io Add-On)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This [Hass.io](https://www.home-assistant.io/hassio/) add-on integrates [Lutron's](http://lutron.com/) original RadioRA Classic (aka legacy or RadioRA 1) light switches and zone controls with [Home Assistant](https://www.home-assistant.io/) by packaging up [Homemation's RadioRA Classic Smart Bridge](https://github.com/homemations/SmartThings). The host running Hass.io with the RadioRA Classic Smart Bridge must be connected via RS-232 cable to the RadioRA Classic hardware interface.

Note: Home Assistant 0.87 or later is required for native SmartThings support (vs a more complex MQTT bridge setup).

### Required Hardware

* Lutron [RadioRA Classic RS232 Serial Interface](http://www.lutron.com/TechnicalDocumentLibrary/044005c.pdf) hardware interface (RA-RS232) or [RadioRA Chronos System Bridge](http://www.lutron.com/TechnicalDocumentLibrary/044037b.pdf) (RA-SBT-CHR)
* server running [Hass.io](https://www.home-assistant.io/hassio/)
* RS232 serial cable wired from RadioRA Classic hardware interface to Hass.io host (e.g. USB male serial adapter or Pi GPIO pints with MAX3232 RS232 male adapter)

See the [Homemation's Lutron RadioRA Classic Bridge](https://github.com/homemations/SmartThings) for details on hardware setup, SmartThings groovy script installs, as well as what features are supported. 

Note: the initial RadioRA Classic Smart Bridge currently only supports Lutron dimmers, switches and zones.

### Hass.io Setup

1. In the Hass.io "Add-On Store" on your Home Assistant, add the repository URL:
<pre>
     https://github.com/rsnodgrass/hassio-addons
</pre>

2. Find the "RadioRA Classic Smart Bridge" in the add-ons and click Install

3. Follow [Homemations instructions](https://github.com/homemations/SmartThings) on how to add the SmartApp and Device Handler in SmartThings. You can manage the SmartApp and Device Handler via the [SmartThings Groovy IDE](https://graph.api.smartthings.com/).

4. Set the add-on's "tty" config option to the tty device on the Hass.io host connected to the RA-RS232 hardware (e.g. /dev/ttyUSB0 for USB serial adapter; default is /dev/ttyAMA0 for a Raspberry Pi GPIO serial port)

### Configuration

Configure each Lutron RadioRA Classic zone/switch using the built-in SmartThings integration with Home Assistant version 0.87 and newer. You must pair all light switches/dimmers into your RA-RS232 hardware adapter per Lutron's instructions. You must also have [configured the SmartThings integration with Home Assistant](https://www.home-assistant.io/components/smartthings/).
