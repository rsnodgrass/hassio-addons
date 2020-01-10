# SOcket CAT (socat) Multipurpose Relay Hass.io Add-On

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**NOT YET WORKING**

This [Hass.io](https://www.home-assistant.io/hassio/) add-on provides support for easily configuring
relay connections to a wide variety of remote network exposed devices by using `socat`. By design, this has
been limited to support pseudo-terminal (pty) dervices only, for the following reasons:

* the goal was to expose virtual tty devices to HA components that rely on reading/writing to local /dev/tty* for communicating with devices
* for security reasons (e.g. no ability to start listeners or interact with the local filesystem on a Home Assistant instance)


#### Use Cases

* communicating to RS232 serial devices using the IP2SL remote serial connection protocol
* communicating to hardware devices exposed via ser2net

### Hass.io Add-on Installation

1. In the Hass.io "Add-On Store" on your Hass.io based Home Assistant server, add this repository URL:
<pre>
     https://github.com/rsnodgrass/hassio-addons
</pre>

2. Find the "SOcket CAT (socat) Multipurpose Relay" in the list of add-ons and click Install

### Configuration

Example config in Hass.io:

```
pty:
  - dev: stereo
    connection: "typ:10.10.1.33:4999"
  - dev: pool-controller
    connection: "typ:10.10.1.12:5002"
    options: pass additional options to socat
```

This will translate into executing on Home Assistant:

```
% socat pty,link=$HOME/dev/stereo,waitslave tcp:10.10.1.33:4999
% socat pty,link=$HOME/dev/pool-controller,waitslave tcp:10.10.1.12:5002
```

## Debugging

Log files are XXX

This also supports Hass.io log levels, with setting info and debug levels increasing the level of log output.

### See Also

- [Virtual IP2SL](https://github.com/rsnodgrass/virtual-ip2sl)
- [socat](https://linux.die.net/man/1/socat)
- [ser2net](https://linux.die.net/man/8/ser2net)
