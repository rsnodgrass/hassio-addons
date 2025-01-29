# Keepalived Home Assistant Add-On

![Project Stage][project-stage-shield]
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)
[![Support on Patreon][patreon-shield]][patreon]

[![Community Forum][forum-shield]][forum]

Home Assistant add-on for [keepalived](https://github.com/shawly/docker-keepalived) to support Virtual Router Redundancy Protocol (VRRP) for load balancing and high availability. This is very useful when running a DNS server add-on on the Home Assistant host, such as [AdGuard Home](https://github.com/hassio-addons/addon-adguard-home) or PiHole, as well as a second instance on another server. **IDEALLY, in the future this would get merged into `hassio-addons/addon-keepalived`**.

Once installed, if you go to 'Settings > System > Network > Configure network interface' in Home Assistant, the IP address for the dynamically created interface that keepalived defined should be listed.

This currently wraps the Docker Keepalived package [shawly/docker-keepalived](https://github.com/shawly/docker-keepalived), but that may change over time if there is a more supported Docker keepalived project.

To avoid IP address conflicts on a LAN with DHCP setup, either set the keepalived IP address outside of the managed IP range *OR* create a DHCP reservation for a fake device MAC so that the IP address is not assigned to another device. For example, create a reservation for the MAC `00:00:00:DB:DB:DB` within the DHCP server for the keepalived interface.

### Support

**There is NO support for this add-on. Feel free to open a pull request if you want to fix any bugs and help maintain this image. Otherwise you are out of luck (for now at least).**

For community support, see [HA discussion group](https://community.home-assistant.io/t/using-keepalived-in-a-hassos-installation/404185/5).

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


#### Example /config/keepalived.conf for Home Assistant

```
# /config/keepalived.conf for Home Assistant

global_defs {
  # router_id dns-homeassistant  # hostname is used by default
}

vrrp_instance dns_cluster {
  state MASTER           # Home Assistant host is setup as primary
  virtual_router_id 53   # convention to prefer port as the vrid (53=DNS)

  priority 100           # priority on the secondary must be lower than the primary DNS server

  interface end0
  virtual_ipaddress {
    192.168.1.53 dev end0  # MUST match interface above (otherwise listens on ALL interfaces)
  }

  #authentication {
  #  auth_type PASS
  #  auth_pass rand0m_passw0rd
  #}
}

# UDP DNS lookups
virtual_server 192.168.1.53 53 {
  protocol UDP
  delay_loop 5
  lb_algo wrr # weighted round robin

  real_server 192.168.1.22 53 {
    weight 100
    DNS_CHECK {
      name example.com
    }
  }

  real_server 192.168.1.33 53 {
    weight 100
    DNS_CHECK {
      name example.com
    }
  }
}

# TCP DoH DNS lookups
virtual_server 192.168.1.53 53 {
  protocol TCP
  delay_loop 5
  lb_algo wrr # weighted round robin

  real_server 192.168.1.22 53 {
    weight 100
    TCP_CHECK {
      connect_timeout 3
      connect_port 53
    }
  }

  real_server 192.168.1.33 53 {
    weight 100
    TCP_CHECK {
      connect_timeout 3
      connect_port 53
    }
  }
}
```

### See Also

* [Pi-hole failover using Keepalived](https://davidshomelab.com/pi-hole-failover-with-keepalived/)

### Credits

* [https://github.com/shawly/docker-keepalived](https://github.com/shawly/docker-keepalived)
* [Philipp Schmitt](https://github.com/pschmitt/home-assistant-addons) for add on this is based on, which used the no-longer maintained and many years out of date [osixia/docker-keepalived](https://github.com/osixia/docker-keepalived).


[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg
[forum]: https://community.home-assistant.io/t/using-keepalived-in-a-hassos-installation/404185/5
[patreon]: https://www.patreon.com/rsnodgrass
[patreon-shield]: https://frenck.dev/wp-content/uploads/2019/12/patreon.png
[project-stage-shield]: https://img.shields.io/badge/project%20stage-production%20ready-brightgreen.svg
