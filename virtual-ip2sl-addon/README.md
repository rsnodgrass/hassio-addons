# Virtual IP2SL (IP to Serial)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)

Provides bidirectional TCP-to-serial access to physical serial ports connected to the
host running this microservice by emulating an iTach IP to Serial (IP2SL). Each instance
of the Virtual IP2SL microservice can expose up to eight physical RS232 serial ports.

This wraps the [standalone Virtual IP2SL](https://github.com/rsnodgrass/virtual-ip2sl) microservice into an easy-to-install Home Assistant Hass.io Add-on.

Some improvements to error handling and dealing with conditions like missing serial devices still need to be implemented, but would be good to get feedback from other users. Also the multicast discovery beacon does not seem to be propagating beyond the Docker container (but manual IP and port configuration works fine).

#### Install as a Hass.io Add-on

1. In the Hass.io "Add-On Store" on your Home Assistant server, add this repository URL:
<pre>
     https://github.com/rsnodgrass/hassio-addons
</pre>

2. Find "__Virtual IP2SL (IP to Serial)__" in the list of add-ons and click Install

## Hass.io Configuration

See [additional standalone configuration](https://github.com/rsnodgrass/virtual-ip2sl) for additional discussion of
options for how Virtual IP2SL can be configured. 

Since Virtual IP2SL uses YAML for configuration, any JSON configuration
in the Hass.io configuration window is automatically converted to YAML and passed to your
running Virtual IP2SL instance.

Here is a simple example for a single USB serial port on a Raspberry Pi (the default config):

```json
{
	"serial": {
		"1": {
			"path": "/dev/ttyUSB0",
			"baud": "9600"
		}
	}
}
```

## Community Support

Links to Home Assistant support forums:

* https://community.home-assistant.io/t/itach-ip2sl/28805
