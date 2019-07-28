# Virtual Flex IP2SL (IP to Serial)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)

*NOT YET IMPLEMENTED*

This emulates a Global Caché iTach Flex IP2SL (IP to Serial) to provide bidirectional
TCP-to-serial access to physical serial ports connected to the host running
this microservice. By implementing the iTach Flex TCP API, this allows for exposes
up to eight physical RS232/RS485 serial ports per running microservice instance.

I decided to build this after having physical USB to serial adapters hooked up to a
Raspberry Pi, but several client applications that supported RS232 over IP using
the published iTach Flex protocol. While Open Source microservices existed to
simulate the iTach Flex IR protocols, none implemented the serial interface. This
was built using a [StarTech ICUSB232I 8-port USB serial adapter](https://amazon.com/StarTech-com-USB-Serial-Adapter-Hub/dp/B009AT5TB2) as well as native Raspberry Pi GPIO
pin outs.

While this microservice is built as a Docker container (with additional support for
making it a plug-and-play [HASS.IO](https://www.home-assistant.io/hassio/) add-on
for Home Assistant](https://www.home-assistant.io/)), this can just as easily be
executed as a standalone server.

#### Install as a Hass.io Add-on

1. In the Hass.io "Add-On Store" on your Home Assistant server, add this repository URL:
<pre>
     https://github.com/rsnodgrass/hassio-addons
</pre>

2. Find the "Virtual Flex IP2SL (IP to Serial)" in the list of add-ons and click Install

# Configuration

By default, this is configured to open ports for eight USB to serial port adapters
with an assortment of baud rates. However, you will want to configure this to
your exact use cases. Additionally, you can comment out any ports you do not
want accessible.

See the "[iTach Flex TCP API Specification](https://www.globalcache.com/files/releases/flex-16/API-Flex_TCP_1.6.pdf)"
PDF manual for the available configuration values for each serial port.

```yaml
serial:
  1: # port 1
    path: /dev/ttyUSB0
    baud: 9600,
    flow: FLOW_NONE, # flowcontrol = RS232
    parity: PARITY_NO,
    stop_bits: STOPBITS_1
  2: 
    path: /dev/ttyUSB1
    baud: 9600,
    flow: FLOW_NONE, # flowcontrol = RS232
    parity: PARITY_NO,
    stop_bits: STOPBITS_1
  3: 
    path: /dev/ttyUSB2
    baud: 14400,
    flow: FLOW_NONE, # flowcontrol = RS232
    parity: PARITY_NO,
    stop_bits: STOPBITS_1
  4: 
    path: /dev/ttyUSB3
    baud: 14400,
    flow: FLOW_NONE, # flowcontrol = RS232
    parity: PARITY_NO,
    stop_bits: STOPBITS_1
  5: 
    path: /dev/ttyUSB4
    baud: 115200,
    flow: FLOW_NONE, # flowcontrol = RS232
    parity: PARITY_NO,
    stop_bits: STOPBITS_1
  6:
    path: /dev/ttyUSB5
    baud: 115200,
    flow: FLOW_NONE, # flowcontrol = RS232
    parity: PARITY_NO,
    stop_bits: STOPBITS_1
  7:
    path: /dev/ttyUSB6
    baud: 115200,
    flow: FLOW_NONE, # flowcontrol = RS232
    parity: PARITY_NO,
    stop_bits: STOPBITS_1
  8:
    path: /dev/ttyUSB7
    baud: 115200,
    flow: DUPLEX_FULL, # duplex = RS485
    parity: PARITY_NO,
    stop_bits: STOPBITS_1
```

### Example TTY Paths

| Serial Path        | Description                                         |
| ------------------ | --------------------------------------------------- |
| /dev/ttyS0         | Raspberry Pi mini UART GPIO                         |
| /dev/ttyAMA0       | Raspberry Pi GPIO pins 14/15 (pre-Bluetooth RPi 3)  |
| /dev/serial0       | RPi 3/RPi 4 serial port alias 1                     |
| /dev/serial1       | RPi 3/RPi 4 serial port alias 2                     |
| /dev/tty.usbserial | typical MacOS USB serial adapter                    |
| /dev/ttyUSB0       | USB serial adapter 1                                |
| /dev/ttyUSB1       | USB serial adapter 2                                |
| /dev/ttyUSB2       | USB serial adapter 3                                |

### Network Ports

The Virtual IP2SL listens on a variety of TCP ports, both for controlling the service
as well as the configuration for each serial port interface. Data sent to any of these
ports is relayed directly out the RS232 serial port associated with that TCP port in
configuration. Similarly, any data received from the RS232 will be written to the TCP
port. The RS232 ports are defaulted to /dev/ttyUSB0 through /dev/ttyUSB7.

| TCP Port | Description                            | Default TTY  |
| -------- | -------------------------------------- | ------------ |
| 4998     | iTach Flex command and control port    |              |
| 4999     | raw TCP port to the first serial port  | /dev/ttyUSB0 |
| 5000     | ... second serial port                 | /dev/ttyUSB1 |
| 5001     | ... third serial port                  | /dev/ttyUSB2 |
| 5002     | ... fourth serial port                 | /dev/ttyUSB3 |
| 5003     | ... fifth serial port                  | /dev/ttyUSB4 |
| 5004     | ... sixth serial port                  | /dev/ttyUSB5 |
| 5005     | ... seventh serial port                | /dev/ttyUSB6 |
| 5006     | raw TCP port to the eighth serial port | /dev/ttyUSB7 |

For enhanced security, it is recommended disabling via configuration any ports
that are not in use.

# TODO

* extend API to support [GC-100](https://www.globalcache.com/files/docs/API-GC-100.pdf)
* ensure client emulation compatibility for GC-100-xx, iTach IP2SL, or Flex
* implement serial communication
* implement web UI (show config, statistics)

#### Community Engagement

Links to active community engagement around iTach Flex integrations:

* (https://community.home-assistant.io/t/itach-ip2sl/28805)

# See Also

* [Home Assistant GC100](https://www.home-assistant.io/components/gc100)
* [iTach Flex TCP API Specification v1.6](https://www.globalcache.com/files/releases/flex-16/API-Flex_TCP_1.6.pdf)
  (earlier [v1.5 specificaiton](https://www.globalcache.com/files/docs/API-iTach.pdf))
* [iTach IP2IR Infrared Emulator](https://github.com/probonopd/ESP8266iTachEmulator/)
* [iTach TCP/IP to Serial (RS232) IP2IR specs](https://www.globalcache.com/products/itach/ip2slspecs/)
* [Flex specs](https://www.globalcache.com/products/flex/flc-slspec/)
