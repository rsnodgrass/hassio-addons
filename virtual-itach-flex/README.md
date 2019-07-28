# Virtual iTach Flex Serial Adapter

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


# Configuration

```yaml
serial:
  1: # port 1
    path: /dev/ttyUSB0
    baud: 115200,
    flow: FLOW_NONE, # flowcontrol = RS232
    parity: PARITY_NO,
    stop_bits: STOPBITS_1
  2: 
    path: /dev/ttyUSB1
    baud: 115200,
    flow: FLOW_NONE, # flowcontrol = RS232
    parity: PARITY_NO,
    stop_bits: STOPBITS_1
  3: 
    path: /dev/ttyUSB2
    baud: 115200,
    flow: FLOW_NONE, # flowcontrol = RS232
    parity: PARITY_NO,
    stop_bits: STOPBITS_1
  4: 
    path: /dev/ttyUSB3
    baud: 115200,
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
