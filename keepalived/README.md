# Keepalived Home Assistant Add-On

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)

Home Assistant add-on for [keepalived](https://github.com/shawly/docker-keepalived) currently wraps the Docker Keepalived package [shawly/docker-keepalived](https://github.com/shawly/docker-keepalived), but that may change over time if there is a more supported Docker keepalived project.

Once installed, if you go to 'Settings > System > Network > Configure network interface' in Home Assistant, the IP address for the dynamically created interface that keepalived defined should be listed.

This is very useful when running a DNS server add-on on the Home Assistant host, such as AdGuard Home or PiHole, as well as a second instance on another server.

### Support

**There is NO support for this add-on. Feel free to open a pull request if you want to fix any bugs and help maintain this image. Otherwise you are out of luck (for now at least).**

### Install as a Hass.io Add-on

[![Show add-on](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=f14f1480_keepalived&repository_url=https%3A%2F%2Fgithub.com%2Frsnodgrass%2Fhassio-addons)

1. In the Hass.io "Add-On Store" on your Home Assistant server, add this repository URL:
<pre>
     https://github.com/rsnodgrass/hassio-addons
</pre>

2. Find "__Keepalived__" in the list of add-ons and click Install


### Configuration

Example configuration:

```yaml
KEEPALIVED_INTERFACE: end0
KEEPALIVED_VIRTUAL_IP: 192.168.1.53
KEEPALIVED_VIRTUAL_MASK: 24
KEEPALIVED_CHECK_IP: any
KEEPALIVED_CHECK_PORT: 53
KEEPALIVED_VRID: 53
TZ: Etc/UTC
```

### See Also

* [Pi-hole failover using Keepalived](https://davidshomelab.com/pi-hole-failover-with-keepalived/)

### Credits

* [https://github.com/shawly/docker-keepalived](https://github.com/shawly/docker-keepalived)
* [Philipp Schmitt](https://github.com/pschmitt/home-assistant-addons) for add on this is based on, which used the no-longer maintained and many years out of date [osixia/docker-keepalived](https://github.com/osixia/docker-keepalived).
