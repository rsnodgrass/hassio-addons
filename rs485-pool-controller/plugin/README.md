# nodejs-poolController-mqttPlugin

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This plugin adds support to a [nodejs-poolController](https://github.com/tagyoureit/nodejs-poolController/tree/next) server for publishing and receiving pool state updates over MQTT.  The nodejs-poolController server allows you to control Pentair pool equipment via its RS485 port (including IntelliCenter, IntelliTouch, EasyTouch, as well as standalone control of pumps and chlorinators without a physical automation controller).

**NOTE: This plugin requires nodejs-poolCenter version 6.0 or higher.**

To install the plugin follow the instructions in the [Installation and Setup](https://github.com/rsnodgrass/nodejs-poolController-mqtttPlugin/wiki/Installation-and-Setup) wiki.

Notably, this MQTT plugin was created to allow Home Assistant (and other home automation platforms that integrate with MQTT) to interact with nodejs-poolController.  **ScreenLogic is not (yet) supported to nodejs-poolController.**

## See Also

* https://github.com/bwoodworth/hassio-addons/tree/master/pentair-screenlogic


## License

Copyright (C) 2020 Ryan Snodgrass
