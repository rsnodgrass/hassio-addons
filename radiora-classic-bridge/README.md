# RadioRA Classic Smart Bridge (Hass.io Add-On)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This [Hassio](https://www.home-assistant.io/hassio/) add-on integrates [Lutron's](http://lutron.com/) original RadioRA Classic (aka legacy or RadioRA 1) light switches and zone controls with [Home Assistant](https://www.home-assistant.io/) by packaging up [Homemation's RadioRA Classic Smart Bridge](https://github.com/homemations/SmartThings). Note that this requires Home Assistant 0.87 or later as this add-on relies on native SmartThings integration (rather than the added complexity of a MQTT bridge).

Credit goes to Stephen Harris at Homemations for developing the Python-based Lutron RadioRA Classic Bridge server
that SmartThings (and any REST client) can communicate with. The Bridge integrates a Lutron RadioRA Classic serial interface (part #RA-RS232) connected directly via RS-232 cable to the Raspberry Pi or host running the Bridge.

### Required Hardware

* Lutron's [RadioRA RS232 Serial Interface](http://www.lutron.com/TechnicalDocumentLibrary/044005c.pdf) hardware box for RadioRA Classic or the [RadioRA Chronos System Bridge](http://www.lutron.com/TechnicalDocumentLibrary/044037b.pdf) (RA-SBT-CHR)
* Raspberry Pi capable of running [Hassio](https://www.home-assistant.io/hassio/)
* RS232 serial cable to Pi: wire RadioRA RA-RS232 directly to Pi GPIO pins (using a MAX3232 RS232 male adapter) *OR* using a USB male serial adapter

See the [Homemation's Lutron RadioRA Classic Bridge](https://github.com/homemations/SmartThings) for details on hardware setup, SmartThings groovy script installs, as well as what features are supported. Note, the initial Lutron RadioRA Manager release only supports dimmers, switches and zones.

### Hass.io Setup

1. In the Hass.io "Add-On Store" on your Home Assistant instance, add this repository URL:
<pre>
     https://github.com/rsnodgrass/hassio-addons
</pre>
2. Find the "RadioRA Classic Smart Bridge" in the add-ons and click Install
3. Follow [Homemations instructions](https://github.com/homemations/SmartThings) on how to add the SmartApp and Device Handler in SmartThings. You can manage the SmartApp and Device Handler via the [SmartThings Groovy IDE](https://graph.api.smartthings.com/).
4. Set the add-on's "tty" config option to the tty device on the Raspberry Pi connected to the RA-RS232 hardware (e.g. /dev/ttyUSB0 for USB serial adapter; default is /dev/ttyAMA0 for GPIO serial port)

### Configuration

Configure each Lutron RadioRA Classic zone/switch using the built-in SmartThings integration with Home Assistant version 0.87 and newer. Reminder that you must pair all light switches/dimmers into your RA-RS232 hardware adapter per Lutron's instructions. You must also have [configured the SmartThings integration with Home Assistant](https://www.home-assistant.io/components/smartthings/).
