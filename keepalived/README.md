# Keepalived Home Assistant Add-On

![Project Stage][project-stage-shield]
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)
[![Support on Patreon][patreon-shield]][patreon]

[![Community Forum][forum-shield]][forum]

Home Assistant add-on for [keepalived](https://github.com/shawly/docker-keepalived) to support Virtual Router Redundancy Protocol (VRRP) for load balancing and high availability. This is very useful when running a DNS server add-on on the Home Assistant host, such as [AdGuard Home](https://github.com/hassio-addons/addon-adguard-home) or PiHole, as well as a second instance on another server. **IDEALLY, in the future this would get merged into `hassio-addons/addon-keepalived`**.

This currently wraps the Docker Keepalived package [shawly/docker-keepalived](https://github.com/shawly/docker-keepalived), but that may change over time if there is a more supported Docker keepalived project.

## Support

If you have trouble with installation and configuration, visit the [HA keepalived discussion group](https://community.home-assistant.io/t/using-keepalived-in-a-hassos-installation/404185/5). The developers are just volunteers from the community and do not provide any support, so it is best to ask the entire community for help or questions. If you have code improvements, please submit Pull Requests with bug fixes!

## Installation

[![Show add-on](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=f14f1480_keepalived&repository_url=https%3A%2F%2Fgithub.com%2Frsnodgrass%2Fhassio-addons)

To install this in Home Assistant:

1. Go to the "Add-On Store" on your Home Assistant server, add this repository URL:
<pre>
     https://github.com/rsnodgrass/hassio-addons
</pre>

2. Find "__Keepalived__" in the list of add-ons and click Install

## Configuration

### Step 1: Home Assistant Setup

To setup Keepalived HA add-on, a '/config/keepalived.conf' needs to exists on the Home Assistant host that has all the custom configuration. The condfig can vary greatly depending on the use case. However, the following is an example `/config/keepalived.conf` from enabling Adguard Home add-on for Home Assistant to join a highly-available cluster of DNS servers in my homelab.

```
# /config/keepalived.conf for DNS running on Home Assistant (e.g. Adguard or PiHole DNS add-on)

global_defs {
  # router_id dns-homeassistant  # hostname is used by default
}

vrrp_instance dns_cluster {
  state MASTER            # Home Assistant host is setup as primary
  virtual_router_id 53    # convention to prefer port as the vrid (53=DNS)

  priority 100            # priority on all secondary (BACKUP) must < the primary DNS server (aka MASTER)

  interface end0
  virtual_ipaddress {
    192.168.1.2/24 dev end0  # MUST match interface above (otherwise listens on ALL interfaces)
  }

  #authentication {
  #  auth_type PASS
  #  auth_pass rand0m_passw0rd
  #}
}

# UDP DNS lookups
virtual_server 192.168.1.2 53 {
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
virtual_server 192.168.1.2 53 {
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

### Step 2: Confirm New Virtual IP is Exposed by Home Assistant

Once installed and running, if you go to 'Settings > System > Network > Configure network interface' in Home Assistant, the IP address for the virtual interface that you created in `keepalived.conf` should be listed.

### Step 3: DHCP Reservation for Virtual IP to Avoid Collisions (Optional)

To avoid IP address conflicts on a LAN with DHCP setup, either set the keepalived IP address outside of the managed IP range *OR* create a DHCP reservation for a fake device MAC so that the IP address is not assigned to another device. For example, create a reservation for the MAC `00:00:00:DB:DB:DB` within the DHCP server for the keepalived interface. In the example `keepalived.conf` above this means creating a reservation for `192.168.1.2`.

## See Also

* [Pi-hole failover using Keepalived](https://davidshomelab.com/pi-hole-failover-with-keepalived/)

## Credits

* [https://github.com/shawly/docker-keepalived](https://github.com/shawly/docker-keepalived)
* [Philipp Schmitt](https://github.com/pschmitt/home-assistant-addons) for add on this is based on, which used the no-longer maintained and many years out of date [osixia/docker-keepalived](https://github.com/osixia/docker-keepalived).


[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg
[forum]: https://community.home-assistant.io/t/using-keepalived-in-a-hassos-installation/404185/5
[patreon]: https://www.patreon.com/rsnodgrass
[patreon-shield]: https://img.shields.io/endpoint.svg?url=https%3A%2F%2Fshieldsio-patreon.vercel.app%2Fapi%3Fusername%3Drsnodgrass%26type%3Dpatrons&style=for-the-badge
[project-stage-shield]: https://img.shields.io/badge/project%20stage-production%20ready-brightgreen.svg
