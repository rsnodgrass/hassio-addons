# Xantech Serial Bridge (Hass.io Add-On)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)

Exposes a REST microservice interface that maps to RS232/RS485 serial device interfaces.

While this is a Hass.io Add-on, that is merely semantic packaging around the Docker container for the microservice. The
Docker image can be executed directly.

```
docker build -t RESTful-serial-bridge .
```

This is the THIRD RS232 / RS485 device I've had to integrate in the last few months. Perhaps there
is some simplification/standardization of these wrappers.

Often RS232 devices are not colocated, so you may run multple instances on different hardware that is 
physically connected to each device you want to control.


**NOT YET WORKING**

### TODO

* should this expose MQTT so that events from serial devices get propagated? (rather than polled)
   - or just optionally add broker support? (in addition to REST API) (broker:port)

### Required Hardware

* "server" running Docker to be able to execute container (e.g. RPi running Home Assistant's [Hass.io](https://www.home-assistant.io/hassio/) hypervisor)
* connection to a hardware or network serial interface to the physical hardware device

### Hass.io Add-on Installation

1. In the Hass.io "Add-On Store" on your Home Assistant server, add this repository URL:
<pre>
     https://github.com/rsnodgrass/hassio-addons
</pre>

2. Find the "Serial Smart Bridge" in the list of add-ons and click Install

### Configuration

### See Also

* [Monoprice 6-zone amp API](https://github.com/jnewland/mpr-6zhmaut-api)



# Xantech Multi-Zone Audio Amplifiers and Controllers

Support for Xantech multi-zone matrix audio amplifiers and controllers.

# Examples

You can easily test this from the command line:

```
curl http://localhost:5000/api/xantech/zones/1
```

```json
{"zone": "1"}
```

Mute zone 4 of the amplifier:

```
curl -X POST http://localhost:5000/api/xantech/zones/1/mute/on
```

# Supported Hardware

The following 8-zone matrix audio amplifiers/controllers are supported:

- MRAUDIO8X8 / MRAUDIO8X8m
- MRC88 / MRC88m
- MX88 / MX88a / MX88ai / MX88vi
- Monoprice MPR-SG6Z (possibly)

### Unsupported

The following do not seem to support the Xantech multi-zone matrix audio RS232 protocol:

- MRAUDIO4X4
- MRC44 / MRC44CTL

# See Also

* [Home Assistant integration](https://github.com/rsnodgrass/hass-integrations/tree/master/custom_components/xantech_mza)
