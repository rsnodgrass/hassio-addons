import os
import re
import uuid
import time

import logging
import threading
import socket

log = logging.getLogger(__name__)

MULTICAST_PORT = 9131
MULTICAST_IP   = '239.255.250.250'
MULTICAST_TTL  = 2 # after TWO network hops the beacon packet should be discarded

# Implements a version of the AMX Beacon device discovery protocol with periodic heartbeats
class AMXDiscoveryBeacon():
    def __init__(self, config):
        self._config = config
        self._beacon_interval = 5 # heartbeat every 10 seconds

        self._thread = threading.Thread(target=self.heartbeat, args=())
        self._thread.daemon = True
        self._thread.start()

    def get_mac(self):
        return ''.join(re.findall('..', '%012x' % uuid.getnode())).upper()

    def get_host(self):
        # In "production", this must be externally accessible and routable
        # IP address (not 0.0.0.0 or localhost) so clients can discover and 
        # communicate with this instance.
        host = '0.0.0.0' # default for testing

        if ('ip2sl' in self._config and 'ip' in self._config['ip2sl']):
            host = self._config['ip2sl']['ip']

        # allow overridding discovered/configured IP address with ENV variable
        host = os.getenv('IP2SL_SERVER_HOST', host) 
        return host

    def heartbeat(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

        # iTach Flex discovery beacon is a AMX-styles multicast UDP packet sent to IP 239.255.250.250, port 9131.
        data = {
            'UUID'       : f"VirtualIP2SL_{self.get_mac()}", # required for IP as unique identifer, could be UUID=GlobalCache_
            'SDKClass'   : 'Utility',            # required
            'Make'       : 'GlobalCache',        # required
            'Model'      : 'iTachFlexEthernet',  # required; note GC-100-12 for legacy model
            'Config-URL' : f"http://{self.get_host()}",
            'Revision'   : '710-2000-15',
            'Pkg_Level'  : '', # "GCPK001",
            'PCB_PN'     : '025-0033-10',
            'Status'     : 'Ready'
            }
        heartbeat_packet = "AMXB" + ''.join(F"<-{k}={v}>" for (k,v) in data.items())

        while True:
            log.debug(f"Broadcasting heartbeat beacon: {heartbeat_packet}")
            sock.sendto(b"{heartbeat_packet}\r", (MULTICAST_IP, MULTICAST_PORT))
            time.sleep(self._beacon_interval)