# Virtual IP2SL (IP to Serial)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)

*NOT YET IMPLEMENTED*

Provides bidirectional TCP-to-serial access to physical serial ports connected to the
host running this microservice by emulating a iTach Flex IP to Serial (IP2SL). Each instance
of the Virtual IP2SL microservice can expose up to eight physical RS232 serial ports.

I decided to build this after having physical USB to serial adapters hooked up to a
Raspberry Pi (such as the 
[StarTech ICUSB232I 8-port USB serial adapter](https://amazon.com/StarTech-com-USB-Serial-Adapter-Hub/dp/B009AT5TB2?tag=carreramfi-20) and native Raspberry Pi GPIO pin outs), but had several iOS and other client applications 
which supported RS232 over IP using the published iTach Flex protocol. While Open
Source projects existed to emulate iTach Flex IR devices, none implemented raw access
to serial ports via TCP. Since some of my RS232/RS485 devices aren't colocated with my
Raspberry Pi, I will also need to buy several [Global Caché iTach Flex WF2IP](/amazon.com/Global-Cache-iTach-Wi-Fi-Serial/dp/B0051BU42W?tag=carreramfi-20) hardware devices to communicate with everything.

Built as a Docker container (with additional support for
making it a plug-and-play [HASS.IO](https://www.home-assistant.io/hassio/) add-on
for Home Assistant](https://www.home-assistant.io/)), this can also easily be
used as a standalone server.

#### Install as a Hass.io Add-on

1. In the Hass.io "Add-On Store" on your Home Assistant server, add this repository URL:
<pre>
     https://github.com/rsnodgrass/hassio-addons
</pre>

2. Find the "Virtual IP2SL (IP to Serial)" in the list of add-ons and click Install

## Configuration

By default, the Virtual IP2SL is configured to open a single port attached 
at 9600 baud to one USB serial port adapter on //dev/ttyUSB0. However, a
wide variety of serial port configurations are possible, up to eight
serial ports per Virutal IP2SL instance.

Below is an example of four USB serial ports connected.
See the "[iTach Flex TCP API Specification](https://www.globalcache.com/files/releases/flex-16/API-Flex_TCP_1.6.pdf)"
PDF manual for the available configuration values for each serial port.

```yaml
serial:
  1: # port 1
    path: /dev/ttyUSB0
    baud: 9600
    flow: FLOW_NONE
    timeout: 4 # optional, default = 5 seconds

  2: 
    path: /dev/ttyUSB1
    baud: 9600
    flow: FLOW_HARDWARE

  3: 
    path: /dev/ttyUSB2
    baud: 14400

  4: 
    path: /dev/ttyUSB3
    baud: 115200
```

#### Network Ports

This microservice implements the open AMX Discovery Beacon protocol, raw TCP sockets to 
RS232 serial ports, and a TCP Port exposing the iTach command protocol.

The Virtual IP2SL listens on a variety of TCP ports, both for controlling the service
as well as the configuration for each serial port interface. Data sent to any of these
ports is relayed directly out the RS232 serial port associated with that TCP port in
configuration. Similarly, any data received from the RS232 will be written to the
TCP port.

| TCP Port | Description                              |
| -------- | ---------------------------------------- |
| 4998     | iTach Flex TCP API command/control port  |
| 4999     | raw TCP port to the first serial port    |
| 5000     | ... second serial port                   |
| 5001     | ... third serial port                    |
| 5002     | ... fourth serial port                   |
| 5003     | ... fifth serial port                    |
| 5004     | ... sixth serial port                    |
| 5005     | ... seventh serial port                  |
| 5006     | raw TCP port to the eighth serial port   |

* For security, it is recommended disabling any ports that are not in use.
If no configuration exists for a given serial port (1-8), the associated TCP port
will not be opened.

#### Example TTY Paths

The following are a variety of example TTY paths for different serial port interfaces:

| Serial Path                 | Description                                         |
| --------------------------- | --------------------------------------------------- |
| /dev/ttyS0                  | Raspberry Pi mini UART GPIO                         |
| /dev/ttyAMA0                | Raspberry Pi GPIO pins 14/15 (pre-Bluetooth RPi 3)  |
| /dev/serial0                | RPi 3/RPi 4 serial port alias 1                     |
| /dev/serial1                | RPi 3/RPi 4 serial port alias 2                     |
| /dev/tty.usbserial          | MacOS USB serial adapter                            |
| /dev/ttyUSB0                | USB serial adapter 1                                |
| /dev/ttyUSB1                | USB serial adapter 2                                |
| /dev/tty.usbserial-A501SGSU | StarTach ICUSB232I (8-port) serial port 1 (MacOS)   |
| /dev/tty.usbserial-A501SGSV | StarTach ICUSB232I (8-port) serial port 2 (MacOS)   |

## See Also

#### Relevant Clients

* [iTest for Windows](https://www.globalcache.com/downloads/) and [iTest for MacOS (by Martijn Rijnbeek)](http://www.rmartijnr.eu/itest.html) - tools for connecting and sending test queries
* [Home Assistant GC100](https://www.home-assistant.io/components/gc100)
* [Home Assistant Notifier](https://github.com/tinglis1/home-assistant-custom/tree/master/custom_components/notify) (last updated 2016)

#### Other

* [iTach IP2IR Infrared Emulator](https://github.com/probonopd/ESP8266iTachEmulator/)
* [iTach Flex TCP API Specification v1.6](https://www.globalcache.com/files/releases/flex-16/API-Flex_TCP_1.6.pdf)
  (earlier [v1.5 specificaiton](https://www.globalcache.com/files/docs/API-iTach.pdf))
* [iTach TCP/IP to Serial (RS232) specs](https://www.globalcache.com/products/itach/ip2slspecs/) and [Flex specs](https://www.globalcache.com/products/flex/flc-slspec/)
* Special thanks to [Global Caché](https://www.globalcache.com/products/) for opening and publishing TCP control APIs

## Support

### Community Engagement

Links to active community engagement around iTach Flex integrations:

* https://community.home-assistant.io/t/itach-ip2sl/28805

### Home Assistant Integration

* 

## TODO

NOTE: While this works for my use cases (and most common ones users will encounter),
it would be great to have other contributors help take this to the next level and
implement features, stability improvements, etc.

Ideas of what should be eventually implemented (but no plans by me to add):

* add support for RS485 connections
* web UI console showing details about the config and each port (including metrics)
* emulation compatibility for [GC-100-xx](https://www.globalcache.com/files/docs/API-GC-100.pdf)
* unit tests