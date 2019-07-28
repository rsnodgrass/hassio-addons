# Virtual iTach Flex Serial Adapter

Like the physical iTach Flex serial devices, this supports up to eight simultaenous,
bidirectional TCP-to-serial connections on port 4999.

This is built as a Home Assistant HASS.IO add-on Docker container, however this
can just as easily be used as a standalone server.

The Virtual Adapter listens on ports 4999-5007, depending on configuration.

Data sent to any of these ports is relayed directly out the RS232 serial port associated
with that TCP port in configuration. Similarly, any data received from the RS232 will
be written to the TCP port. The RS232 ports are defaulted to /dev/ttyUSB0 through /dev/ttyUSB7.


# Configuration

```yaml
serial:
	1: /dev/ttyUSB0,
	2: /dev/ttyAMA0, # example: Raspberry Pi direct GPIO mapping
```

# See Also

* [iTach Flex TCP API Specification v1.6](https://www.globalcache.com/files/releases/flex-16/API-Flex_TCP_1.6.pdf)
* (https://github.com/probonopd/ESP8266iTachEmulator/)

# TODO

* implement serial communication
* implement configuration of serial ports
* implement web UI

