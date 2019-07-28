#!/usr/local/bin/python3

import logging

import uuid
import time
import re

import threading
import socket

log = logging.getLogger(__name__)

MULTICAST_IP = '239.255.250.250'
MULTICAST_GROUP = '01:00:5E:7F:FA:FA'
MULTICAST_PORT = 9131

# regarding socket.IP_MULTICAST_TTL
# ---------------------------------
# for all packets sent, after two hops on the network the packet will not 
# be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
MULTICAST_TTL = 2

def get_mac():
    return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

def get_ip():
    return "127.0.0.1"

class HeartbeatBeacon():
    def __init__(self):
        thread = threading.Thread(target=self.heartbeat, args=())
        thread.daemon = True
        thread.start()

    def heartbeat(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

        # the iTach Flex discovery beacon is a multicast UDP packet sent to IP 239.255.250.250, port 9131.
        # AMX beacons must be terminated by a carriage return (‘\r’, 0x0D)
        data = {
            "UUID"       : f"GlobalCache_{get_mac()}", # required for IP as unique identifer, could be UUID=WF2IR_
            "SDKClass"   : "Utility",     # required
            "Make"       : "GlobalCache", # required
            "Model"      : "iTachFlexEthernet", # "iTachWF2IR",  # required
            "Config-URL" : "http://192.168.1.70",
            "Status"     : "Ready"
#            "Revision"   : "710-1001-05",
#            "Pkg_Level"  : "GCPK001",
#            "PCB_PN"     : "025-0026-06", #025-0033-10
            }
        heartbeat_packet = "AMXB" + ''.join(F"<-{k}={v}>" for (k,v) in data.items()) + "\r"
 
        while True:
            log.info(f"Broadcasting heartbeat package: {heartbeat_packet}")
            sock.sendto(b"{heartbeat_packet}", (MULTICAST_IP, MULTICAST_PORT))
            time.sleep(10) # heartbeat every 10 seconds (FIXME: should we add jitter to this?)
