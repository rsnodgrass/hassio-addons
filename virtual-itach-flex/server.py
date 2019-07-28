#!/usr/local/bin/python3
#
# Emulates a GlobalCache IP to serial adapter by passing commands to locally
# configured serial ports.

#import logger

import uuid
import time
import re

import threading
import socket
import socketserver

MULTICAST_IP = '239.255.250.250'
MULTICAST_GROUP = '01:00:5E:7F:FA:FA'
MULTICAST_PORT = 9131

# regarding socket.IP_MULTICAST_TTL
# ---------------------------------
# for all packets sent, after two hops on the network the packet will not 
# be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
MULTICAST_TTL = 2

ITACH_FLEX_TCP_PORT = 5999

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
            print(f"Broadcasting heartbeat package: {heartbeat_packet}")
            sock.sendto(b"{heartbeat_packet}", (MULTICAST_IP, MULTICAST_PORT))
            time.sleep(10) # heartbeat every 10 seconds (FIXME: should we add jitter to this?)

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self._data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self._data)

        if self._data == b"getdevices":
            self.handle_getdevices()
        elif self._data == b"getversion":
            self.handle_getversion()
        elif self._data.startsWith("get_NET"):
            self._handle_get_NET()
        elif self._data.startsWith("get_SERIAL"):
            self._handle_get_SERIAL()
        elif self._data.startsWith("set_SERIAL"):
            self._handle_set_SERIAL()
        else:
            print("Unknown request: {self._data}")

    def send_response(self, response):
        print(f"Sending response: {response}")
        self.request.sendall(b"{response}")

    def handle_getdevices(self):
        response = "\n".join([
                "device,0,0 ETHERNET",
                "device,1,1 SERIAL",
                "endlistdevices"])
        self.send_response(response)

    def handle_getversion(self):
        self.send_response("710-2000-15") # firmware version part number

    def handle_get_NET(self):
        # NET,0:1,<configlock>,<ipsetting>,<ipaddress>,<subnet>,<gateway>
        self.send_response("NET,0:1,LOCKED,STATIC,127.0.0.1,255.255.255.0,127.0.0.1")

    def handle_get_SERIAL(self):
        self.send_response("SERIAL,1:1,115200,FLOW_NONE,PARITY_NO,STOPBITS_1")

    def handle_set_SERIAL(self):
        # set_SERIAL,<module>:<port>
        # set_SERIAL,<module>:<port>,<baudrate>,<flowcontrol/duplex>,<parity>,[stopbits]

        # response: SERIAL,1:1,<baudrate>,<flowcontrol/duplex>,<parity>,<stopbits>
        self.send_response("SERIAL,1:1,115200,FLOW_NONE,PARITY_NO,STOPBITS_1")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def main():
    beacon = HeartbeatBeacon()

    server = ThreadedTCPServer(("localhost", ITACH_FLEX_TCP_PORT), ThreadedTCPRequestHandler)

    # start a thread with the server -- that thread will start a new thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    #server_thread.daemon = True # exit the server thread when the main thread terminates
    #server_thread.start()
    #print("Server loop running in thread:", server_thread.name)

    # FIXME: should we limit the maximum threads that can be created (e.g. max simultaneous clients)

    server.serve_forever()

#    server.shutdown()
#    server.server_close()

if __name__ == '__main__':
  main()

# FIXME: add the port 80 server for web UI management?
