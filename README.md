# Home Assistant Extensions

## Add-ons

Please follow the procedures highlighted in the [Home Assistant website](https://home-assistant.io/hassio/installing_third_party_addons). Use the following URL to add this repository:  https://github.com/rsnodgrass/hassio-addons/

[![Add repository on my Home Assistant][repository-badge]][repository-url]

| Hass.io Add-On                      | Description | Show |
| ----------------------------------- | ----------- |------|
| **[Virtual IP2SL (IP-to-Serial)](https://github.com/rsnodgrass/hassio-addons/tree/master/virtual-ip2sl-addon)** | Enables remote bidirectional TCP communication to physical serial ports by implementing the iTach Flex IP to Serial (IP2SL) protocol. *(can be used as Hass.io add-on or standalone)* | [![Show add-on](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=746b492e_virtual-ip2sl&repository_url=https%3A%2F%2Fgithub.com%2Frsnodgrass%2Fhassio-addons) |
| **[Keepalived](keepalived)** | Keepalived add-on for running highly available services, such as DNS, using the Virtual Router Redundancy Protocol (VRRP). | [![Show add-on](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=f14f1480_keepalived&repository_url=https%3A%2F%2Fgithub.com%2Frsnodgrass%2Fhassio-addons) |

## Custom Integrations

Use [Home Assistant Community Store (HACS)](https://github.com/custom-components/hacs) when installing these integrations:

| Component                        | Description |
| -------------------------------- | ----------- |
| [Lunos Ventilation](https://github.com/rsnodgrass/hass-lunos) | control Lunos HRV and ventilation systems |
| [Pool Math](https://github.com/rsnodgrass/hass-poolmath) | sensors for data collected in Pool Math by Trouble Free Pool |
| [Xantech Matrix Audio Control](https://github.com/rsnodgrass/hass-xantech) | control multi-zone audio controllers/amplifiers with RS232 serial control using Xantech (and other brand) protocols |
| [AnthemAV Serial Control](https://github.com/rsnodgrass/hass-anthemav-serial) | control Anthem receivers/pre-amps that only support RS232 serial control |

## Automation Blueprints

[Automation blueprints](https://github.com/rsnodgrass/home-assistant-blueprints) for Home Assistant.

## UI Cards (Lovelace)

* [Water Heater Card](https://github.com/rsnodgrass/water-heater-card)
* Compass Card — taken over by tomvanswam@ [Compass Card](https://github.com/tomvanswam/compass-card) with awesome improvements



[repository-badge]: https://img.shields.io/badge/Add%20repository%20to%20my-Home%20Assistant-41BDF5?logo=home-assistant&style=for-the-badge
[repository-url]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Frsnodgrass%2Fhassio-addons
