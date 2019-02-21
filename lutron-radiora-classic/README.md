# Lutron RadioRA Classic SmartThings Gateway Add-On for Hass.io

This [Hassio](https://www.home-assistant.io/hassio/) add-on integrates [Lutron's](http://lutron.com/) original RadioRA Classic (aka legacy or RadioRA 1) light switches and zone controls with [Home Assistant](https://www.home-assistant.io/) by packaging up [Homemations Lutron RadioRA Manager](https://github.com/homemations/SmartThings). Note that this requires Home Assistant 0.87 or later as this add-on relies on native SmartThings integration (rather than the added complexity of a MQTT bridge).

Credit goes to Stephen Harris at Homemations for developing the  Python based Lutron RadioRA Gateway to expose RESTful APIs that a SmartThings hub can communicate with. The Python server communicates with a Lutron RadioRA Classic serial interface (part #RA-RS232), connected directly via RS-232 cable to the Raspberry Pi, with a SmartThings hub running on a shared local network.

### Required Hardware

* Lutron's [RadioRA RS232 Serial Interface](http://www.lutron.com/TechnicalDocumentLibrary/044005c.pdf) for RadioRA Classic
* Raspberry Pi capable of running [Hassio](https://www.home-assistant.io/hassio/)
* RS232 serial cable to Pi: wire RadioRA RA-RS232 directly to Pi gpio pins *OR* use a USB serial adapter

See the [Homemations Lutron RadioRA Manager](https://github.com/homemations/SmartThings) for details on hardware setup, SmartThings groovy script installs, as well as what features are supported. Note, the initial Lutron RadioRA Manager release only supports dimmers, switches and zones.

### Hassio Setup

1. To to the Hass.io "Add-On Store" on your Raspberry Pi and add the repository URL for the Lutron RadioRA Classic integration:
<pre>
     https://github.com/rsnodgrass/SmartThings/tree/master/Lutron%20RadioRA/hassio/repository
</pre>
2. Find the "Lutron RadioRA Classic SmartThings Gateway" in the add-ons and click Install
3. Follow Homemations instructions on how to add the SmartApp and Device Handler in SmartThings. You can manage the SmartApp and Device Handler via the [SmartThings Groovy IDE](https://graph.api.smartthings.com/).

### Configuration

Example Home Assistant configuration.yaml entry:

<pre>switches:
</pre>

Configure each Lutron RadioRA zone/switch using standard SmartThing integration with Home Assistant. Reminder that you must pair all light switches/dimmers into your RA-RS232 hardware adapter per Lutron's instructions. You must also have already [configured the SmartThings integration with Home Assistant](https://www.home-assistant.io/components/smartthings/).

## Security

Note, this opens a port on your local network with a REST server that controls your Lutron RadioRA lighting. Anyone with access to your network could possibly control your lights.

## FIXME

- change default port from 8080 as that is likely to conflict!
- FLASK_SERVER_NAME: 192.168.1.142:8080 (see python/settings.py)
- ensure logs are visible in Hass.io add-on console!