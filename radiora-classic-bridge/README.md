# RadioRA Classic Smart Bridge (Hass.io Add-On)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This [Hass.io](https://www.home-assistant.io/hassio/) add-on integrates [Lutron's](http://lutron.com/) original RadioRA Classic (aka legacy or RadioRA 1) light switches and zone controls with [Home Assistant](https://www.home-assistant.io/) by packaging up [Homemation's RadioRA Classic Smart Bridge](https://github.com/homemations/SmartThings). The host running Hass.io with the RadioRA Classic Smart Bridge must be connected via RS-232 cable to the RadioRA Classic hardware interface.

Note: Home Assistant 0.87 or later is required for native SmartThings support (vs a more complex MQTT bridge setup).

### Required Hardware

![RadioRA Classic Smart Bridge](img/diagram.jpg)

* server running Home Assistant's [Hass.io](https://www.home-assistant.io/hassio/)
* Lutron RadioRA Classic RS232 hardware interface: [RA-RS232](http://www.lutron.com/TechnicalDocumentLibrary/044005c.pdf) or [Chronos System Bridge (RA-SBT-CHR)](http://www.lutron.com/TechnicalDocumentLibrary/044037b.pdf)
* RS232 serial cable (e.g. USB male serial adapter or Pi GPIO pints with MAX3232 RS232 male adapter)

See the [Homemation's Lutron RadioRA Classic Bridge](https://github.com/homemations/SmartThings) for additional hardware details, SmartThings groovy script installation, as well as supported features. 

### Hass.io Setup

1. In the Hass.io "Add-On Store" on your Home Assistant server, add this repository URL:
<pre>
     https://github.com/rsnodgrass/hassio-addons
</pre>

2. Find the "RadioRA Classic Smart Bridge" in the list of add-ons and click Install

3. Follow [Homemations instructions](https://github.com/homemations/SmartThings) to add the SmartApp and Device Handler using the [SmartThings Groovy IDE](https://graph.api.smartthings.com/).

4. On the Hass.io RadioRA Classic Smart Bridge add-on page set the "serial_tty" config option to the tty device path for the serial cable connected the Classic RadioRA hardware interface (e.g. default is /dev/ttyUSB0 for a USB serial adapter; use /dev/ttyAMA0 for Raspberry Pi GPIO).

### Configuration

1. Once the Hass.io Lutron RadioRA Classic Bridge has been installed and is running, Lutron's procedures must be followed to pair each switch/dimmer/zone with the Classic RadioRA RS232 hardware interface (if not already completed). This varies whether the Lutron RA-RS232 or Chronos System Bridge is being used as the hardware interface.

2. Finally, the native [SmartThings integration with Home Assistant](https://www.home-assistant.io/components/smartthings/) must be configured so that Home Assistant can communicate through SmartThings to the Classic RadioRA hardware via SmartThings.
