# Multi-Zone Audio Serial Bridge (Hass.io Add-On)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)

Microservice exposing a REST interface for communicating with multi-zone audio
controllers and amplifiers that support variations of Xantech's original RS232
serial control protocol.

## Required Hardware
 
* multi-zone amplifier or controller that supports variations of the Xantech RS232 serial protocol (see below)
* host machine with a serial cable or network serial adapter to physically connect to a Xantech supported multi-zone amplifier/controller
* host machine for executing the Docker container (e.g. [Raspberry Pi](https://www.raspberrypi.org/) running Home Assistant's [Hass.io](https://www.home-assistant.io/hassio/) hypervisor)

#### Supported Amplifiers/Controllers

| Manufacturer  | Model(s)                        | Zones | Supported |
| ------------- | ------------------------------- |:-----:|:---------:|
| Xantech       | MRAUDIO8X8 / MRAUDIO8X8m        | 8     | YES       |
|               | MRC88 / MRC88m                  | 8     | YES       |
|               | MX88 / MX88a / MX88ai / MX88vi  | 8     | YES       |
|               | MRAUDIO8X8 / MRAUDIO8X8m        | 8     | YES       |
|               | MRAUDIO4X4                      | 4     | *NO*      |
|               | MRC44 / MRC44CTL                | 4     | *NO*      |
| Monoprice     | MPR-SG6Z / 10761                | 6     | *MAYBE*   |
| Dayton Audio  | DAX66                           | 6     | *MAYBE*   |

* The [Monoprice MPR-SG6Z](https://www.monoprice.com/product?p_id=10761) and
  [Dayton Audio DAX66](https://www.parts-express.com/dayton-audio-dax66-6-source-6-room-distributed-whole-house-audio-system-with-keypads-25-wpc--300-585)
  appear to have licensed or copies the serial interface from Xantech. Both Monoprice
  and Dayton Audio use a version of the Xantech multi-zone controller protocol.

While some amplifiers (e.g. Xantech and Monoprice) support expanding the number of zones
by connecting two (or three) amplifiers together, the Multi-Zone Audio Serial Bridge enables
an "unlimited" number of amplifiers to be controlled via a REST interface.

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

2. Find the "Multi-Zone Audio Serial Bridge" in the list of add-ons and click Install

## Configuration

The zone and source names are optionally configurable on the Multi-Zone Audio Serial Bridge
as opposed to on the client side (like in Home Assistant configuration) since there may
be multiple clients that are accessing the Bridge's APIs, for instance a standalone
Alexa, iOS, Apple Watch integrations or directly via a browser. This reduces the
configuration and setup required across multiple client integrations.

```json
{ 
   "zone_names": {
      "1": "Living Room",
      "2": "Kitchen",
      "3": "Master Bedroom",
      "4": "Master Bathroom",
      "5": "Home Theater",
      "6": "Kids Room",
      "7": "Garage",
      "8": "Patio"
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

# Client Registry

Known clients which interface with the Multi-Zone Audio Serial Bridge:

* [Multi-Zone Audio Control add-on](https://github.com/rsnodgrass/hass-integrations/tree/master/custom_components/xantech_mza) for [Home Assistant](https://home-assistant.io)

# Not Yet Implemented

#### Priority

* ability to remote configure or rename zones/sources via the REST API
* add documentation of all the API endpoints and link from here
* look at matrix switching for inspiration: https://www.home-assistant.io/components/blackbird/

#### Unplanned

* allow connecting as many amplifiers via serial ports as possible and controling through a single Bridge instance
* add support for a remote Global Cache iTach Flex IP/Wifi serial interface where the Xantech Serial Bridge can't physically be connected via serial to the amplifier
* configurable "maximum volume" for each zone, which cannot be exceeded by volume control API calls
* virtual master/slave across several connected multi-zone amplifiers (including across multiple brands)
* support publishing state change events to a MQTT broker
* theoretically the Bridge's REST API, design model, and code structure could support other RS232 compatible matrix audio controller protocols (such as the Niles IntelliControl ICS GXR2), but no plans to implement

# See Also

* [Monoprice RS232 serial protocol manual](doc/Monoprice-RS232-Manual.pdf)
* [Monoprice RS232 serial protocol control](doc/Monoprice-RS232-Control.pdf)

#### Alternatives

* [Monoprice mpr-6zhmaut-api NodeJS REST server](https://github.com/jnewland/mpr-6zhmaut-api)
* [Monoprice 10761 iOS and Apple Control control app](https://apps.apple.com/us/app/monoprice-whole-home-audio/id1168858624) (just as a reference, it does not use this bridge)
* [Monoprice Amp Mixer for Windows](https://www.dropbox.com/s/aem6yck98etq9mb/MonoAmpV41.zip?file_subpath=%2FMonoAmpV41%2FMono.jpg)
* [Monoprice Whole Home Audio iOS app](https://apps.apple.com/us/app/monoprice-whole-home-audio/id1168858624)
* [Whole House Audio - Small Price / Big Value](https://chrisschuld.com/2019/05/whole-house-audio/)

#### Community Engagement

Sites with active community engagement around the Xantech, Monoprice, and Daytona AUdio
multi-zone amplifiers:

* (https://www.avsforum.com/forum/36-home-v-distribution/1506842-any-experience-monoprice-6-zone-home-audio-multizone-controller-23.html)
* (http://cocoontech.com/forums/topic/25893-monoprice-multi-zone-audio/)
