# Lutron RadioRA 1 SmartThings Gateway Add-On for Hass.io

This [Hassio](https://www.home-assistant.io/hassio/) add-on integrates [Lutron's](http://lutron.com/)
original RadioRA 1 (version 1) light switch and zone controls with [Home Assistant]
(https://www.home-assistant.io/)
by packaging up [HomeMation's Lutron RadioRA Manager](https://github.com/homemations/SmartThings). 
Note that this requires Home Assistant 0.87 or later as this add-on relies on native SmartThings
integration (rather than the added complexity of a MQTT bridge).

The Lutron RadioRA Gateway was developed by Stephen Harris at HomeMations using Python
to expose RESTful APIs that a SmartThings hub can communicate with. The Python server
communicates with a Lutron RadioRA 1 serial interface (part #RA-RS232), connected directly
via RS-232 cable to the Raspberry Pi, with a SmartThings hub running on a shared
local network.

### Required Hardware

* Lutron's [RadioRA RS232 Serial Interface](http://www.lutron.com/TechnicalDocumentLibrary/044005c.pdf)
* Raspberry Pi capable of running [Hassio](https://www.home-assistant.io/hassio/)
* RS232 Serial interface to Pi: direct wire RadioRA RA-S232 to Pi pins *OR* a USB serial adapter

See the [HomeMation Lutron RadioRA Manager](https://github.com/homemations/SmartThings)
for details on hardware setup, SmartThings groovy script installs, as well as what features
are supported. Note, the initial Lutron RadioRA Manager release only supports dimmers, switches and zones.

### Hassio Setup

1. To to the Hass.io "Add-On Store" on your Raspberry Pi and add the repository URL
   for the Lutron RadioRA 1 integration:

<pre>
     https://github.com/rsnodgrass/SmartThings/tree/master/Lutron%20RadioRA/hassio/repository
</pre>

2. Find the "Lutron RadioRA 1 SmartThings Gateway" in the add-ons and click Install

3. Follow HomeMation's instructions on how to add the SmartApp and Device Handler in
   SmartThings. You can manage the SmartApp and Device Handler via the 
   [SmartThings Groovy IDE](https://graph.api.smartthings.com/).

### Configuration

Edit your Home Assistant configuration.yaml:

<pre>switches:
  - platform: mqtt
    name: "Lutron RadioRA"
</pre>

Add the following to the configuration.yaml for each switch:

<pre>
  - platform: mqtt
    name: "Kitchen Door"
</pre>

Configure each Lutron RadioRA zone/switch using standard SmartThing
integration with Home Assistant.

## Security

Note, this opens a port on your local network with a REST server that
can control your Lutron RadioRA lighting. Anyone who can access your
network could possibly control your lights.

## FIXME

- enable configuration of port...change default from 8080 as that is likely to conflict!
- FLASK_SERVER_NAME: 192.168.1.142:8080 (see python/settings.py)
- ensure logs are visible in Hass.io add-on console!