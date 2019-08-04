import logging

import os
import re
import uuid
import time
import threading
import socket

import util

log = logging.getLogger(__name__)

MULTICAST_PORT = 9131
MULTICAST_IP   = '239.255.250.250'
MULTICAST_TTL  = 2 # after TWO network hops the beacon packet should be discarded

# Implements a version of the AMX Beacon device discovery protocol with periodic heartbeats
class AMXDiscoveryBeacon():
    def __init__(self, config):
        self._config = config

        # heartbeat interval in seconds (default is every 10 seconds); ENV override for testing
        self._beacon_interval = max(1, int(os.getenv('IP2SL_BEACON_INTERVAL', '10')))

        self._console_host = util.get_host(config)
        self._console_port = int(os.getenv('IP2SL_CONSOLE_PORT', 4444))

        self._thread = threading.Thread(target=self.heartbeat, args=())
        self._thread.daemon = True
        self._thread.start()

    def get_mac(self):
        return ''.join(re.findall('..', '%012x' % uuid.getnode())).upper()

    def heartbeat(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

        # iTach Flex discovery beacon is a AMX-styles multicast UDP packet sent to IP 239.255.250.250, port 9131.
        data = {
            'UUID'       : f"VirtualIP2SL_{self.get_mac()}", # required; unique identifer for this instance
            'SDKClass'   : 'Utility',            # required
            'Make'       : 'GlobalCache',        # required
            'Model'      : 'iTachFlexEthernet',  # required; note GC-100-12 for legacy model, or iTachIP2SL for v1.5 API
            'Config-URL' : f"http://{self._console_host}:{self._console_port}",
            'Revision'   : '710-3000-18',
            'Pkg_Level'  : '', # "GCPK001",
            'PCB_PN'     : '025-0034-12',
            'Status'     : 'Ready'
            }
        heartbeat_packet = "AMXB" + ''.join(F"<-{k}={v}>" for (k,v) in data.items())

        while True:
            log.debug(f"Broadcasting heartbeat beacon to {MULTICAST_IP}:{MULTICAST_PORT}: {heartbeat_packet}")
            heartbeat_packet += "\r"
            sock.sendto(heartbeat_packet.encode(), (MULTICAST_IP, MULTICAST_PORT))
            time.sleep(self._beacon_interval)
