# Virtual iTach Flex Serial Adapter

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)

*NOT YET IMPLEMENTED*

Emulates a Global Caché iTach IP to Serial (IP2SL) to provide bidirectional
TCP-to-serial connections to physical serial ports connected to the host running
this microservice. By implementing the iTach Flex TCP API, this allows for exposes
up to eight physical RS232/RS485 serial ports per running microservice instance.

While built as a Docker container (with additional support for making it a plug-and-play
Home Assistant HASS.IO add-on), this can just as easily be executed as a standalone server.

The Virtual Adapter listens on ports 4999-5007, depending on configuration.

Data sent to any of these ports is relayed directly out the RS232 serial port associated
with that TCP port in configuration. Similarly, any data received from the RS232 will
be written to the TCP port. The RS232 ports are defaulted to /dev/ttyUSB0 through /dev/ttyUSB7.

#### Install as a Hass.io Add-on

1. In the Hass.io "Add-On Store" on your Home Assistant server, add this repository URL:
<pre>
     https://github.com/rsnodgrass/hassio-addons
</pre>

2. Find the "Virtual iTach Flex Serial" in the list of add-ons and click Install

# Configuration

By default, this is configured to open ports for eight USB to serial port adapters
with an assortment of baud rates. However, you will want to configure this to
your exact use cases. Additionally, you can comment out any ports you do not
want accessible.

See the "iTach Flex TCP API Specification" PDF manual for the available configuration
values for each serial port.

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

# See Also

* [iTach Flex TCP API Specification v1.6](https://www.globalcache.com/files/releases/flex-16/API-Flex_TCP_1.6.pdf)
* [iTach IP2IR Infrared Emulator](https://github.com/probonopd/ESP8266iTachEmulator/)
* [iTach TCP/IP to Serial (RS232) IP2IR specs](https://www.globalcache.com/products/itach/ip2slspecs/)
* [Flex specs](https://www.globalcache.com/products/flex/flc-slspec/)

# TODO

* implement serial communication
* implement configuration of serial ports
* implement web UI

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

#### Community Engagement

Links to active community engagement around iTach Flex integrations:

* 