# SOcket CAT (socat) Remote Serial Device Hass.io Add-On

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
  - dev: marantz-stereo
    remote_address: "tcp:10.10.1.33:4999"
  - dev: pool-controller
    remote_address: "tcp:10.10.1.12:5002"
    pty_options: "waitslave"
  - dev: monoprice
    remote_address: "tcp:10.10.1.12:4999"
```

This will translate into executing on Home Assistant:

```
% socat -d -d pty,link=$HOME/dev/marantz-stereo tcp:10.10.1.33:4999
% socat -d -d pty,link=$HOME/dev/pool-controller,waitslave tcp:10.10.1.12:5002
% socat -d -d pty,link=$HOME/dev/monoprice tcp:10.10.1.12:4999
```

The `remote_address` option is the second address argument passed into socat.

## Debugging

Log files are XXX

This also supports Hass.io log levels, with setting info and debug levels increasing the level of log output.

### See Also

- [Virtual IP2SL](https://github.com/rsnodgrass/virtual-ip2sl)
- [socat](https://linux.die.net/man/1/socat)
- [ser2net](https://linux.die.net/man/8/ser2net)

## Post Here When Ready

* https://community.home-assistant.io/t/missing-command-like-socat-on-hassio/100362/11
