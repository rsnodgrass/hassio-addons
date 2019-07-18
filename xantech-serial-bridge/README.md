# Xantech Serial Bridge (Hass.io Add-On)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)

Exposes a REST interface that bridges to a serial connected multi-zone amplifier that supports the
Xantech RS232 serial control protocol.  

## Required Hardware

* multi-zone amplifier or controller that supports to the Xantech RS232 serial protocol (see below)
* serial cable or network serial adapter connected to a Xantech supported multi-zone amplifier/controller
* "server" running Docker to be able to execute container (e.g. RPi running Home Assistant's [Hass.io](https://www.home-assistant.io/hassio/) hypervisor)

#### Supported Amplifiers/Controllers

| Manufacturer  | Model(s)                        | Supported |
| ------------- | --------------------------------|:---------:|
| Xantech       | MRAUDIO8X8 / MRAUDIO8X8m        | YES       |
|               | MRC88 / MRC88m                  | YES       |
|               | MX88 / MX88a / MX88ai / MX88vi  | YES       |
|               | MRAUDIO8X8 / MRAUDIO8X8m        | YES       |
|               | MRAUDIO4X4                      | NO        |
|               | MRC44 / MRC44CTL                | NO        |
| Monoprice     | MPR-SG6Z                        | MAYBE *   |

* The Monoprice MPR-SG6Z serial interface appears to be licensed from Xantech, or 
  perhaps Xantech sold its amplifier line to Monoprice. Monoprice amp uses a
  version of the Xantech multi-zone controller protocol.


## Installation

#### Install as a Docker Container

While this is called a Hass.io Add-on, that is merely semantic packaging around a Docker container,
which can also be executed directly.

```bash
docker build -t xantech-serial-bridge .
```

#### Install as a Hass.io Add-on

1. In the Hass.io "Add-On Store" on your Home Assistant server, add this repository URL:
<pre>
     https://github.com/rsnodgrass/hassio-addons
</pre>

2. Find the "Serial Smart Bridge" in the list of add-ons and click Install

## Configuration

```json
{ 
   "zone_names": {
      "1": "Living Room",
      "2": "Kitchen",
      "3": "Master Bedroom",
      "4": "Patio"
   }
}
```

## REST Interface 

#### Command Line Interaction

Show details for zone 1:

```bash
curl http://localhost:5000/xantech/zones/1
```

Response:

```json
```

Mute zone 4:

```bash
curl -X POST http://localhost:5000/xantech/zones/4/mute/on
```

# TODO

* should this expose MQTT so that events from serial devices get propagated? (rather than polled)
   - or just optionally add broker support? (in addition to REST API) (broker:port)
* add documentation of all the API endpoints and link from here

# See Also

* [Home Assistant integration for the Xantech Serial Bridge](https://github.com/rsnodgrass/hass-integrations/tree/master/custom_components/xantech_mza)
* [Monoprice mpr-6zhmaut-api NodeJS REST server](https://github.com/jnewland/mpr-6zhmaut-api)
