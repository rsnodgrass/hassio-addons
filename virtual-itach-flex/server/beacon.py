#!/usr/local/bin/python3
import re
import uuid
import time

import logging
import threading
import socket

log = logging.getLogger(__name__)

MULTICAST_IP    = '239.255.250.250'
MULTICAST_GROUP = '01:00:5E:7F:FA:FA'
MULTICAST_PORT  = 9131
MULTICAST_TTL   = 3 # after three network hops the beacon packet should be discarded

def get_mac():
    return ''.join(re.findall('..', '%012x' % uuid.getnode())).upper()

def get_ip():
    return "127.0.0.1"

# Implements a version of the AMX Beacon device discovery protocol with periodic heartbeats
class AMXDiscoveryBeacon():
    def __init__(self, config):
        self._config = config

        thread = threading.Thread(target=self.heartbeat, args=())
        thread.daemon = True
        thread.start()

    def heartbeat(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

        # must be externally accessible and routable IP (not 0.0.0.0 or localhost)
        ip = get_ip() # FIXME: alternatively use whatever is in config!
#       ip = self._config['server']['ip']

        # iTach Flex discovery beacon is a AMX-styles multicast UDP packet sent to IP 239.255.250.250, port 9131.
        data = {
            "UUID"       : f"GlobalCache_{get_mac()}", # required for IP as unique identifer, could be UUID=WF2IR_
            "SDKClass"   : "Utility",            # required
            "Make"       : "GlobalCache",        # required
            "Model"      : "iTachFlexEthernet",  # required; note GC-100-12 for legacy model
            "Config-URL" : f"http://{ip}",
            "Revision"   : "710-2000-15",
            "Pkg_Level"  : "", # "GCPK001",
            "PCB_PN"     : "025-0033-10",
            "Status"     : "Ready"
            }
        heartbeat_packet = "AMXB" + ''.join(F"<-{k}={v}>" for (k,v) in data.items())

        while True:
            log.debug("Broadcasting heartbeat beacon: %s", heartbeat_packet)
            print(f"Broadcasting heartbeat beacon: {heartbeat_packet}")
            sock.sendto(b"{heartbeat_packet}\r", (MULTICAST_IP, MULTICAST_PORT))
            time.sleep(5) # heartbeat every 10 seconds
