#!/usr/local/bin/python3
#
# Emulates a GlobalCache IP to serial adapter by passing commands to
# locally configured serial ports.

import logging
from flask import Flask

import os
import uuid
import time
import re
import yaml

import threading
import socket
import socketserver

from beacon import HeartbeatBeacon

log = logging.getLogger(__name__)

ITACH_FLEX_COMMAND_TCP_PORT = 4999

app = Flask(__name__)

# general errors
ERR_INVALID_REQUEST      ="ERR 001" # Invalid request. Command not found.
ERR_INVALID_SYNTAX       ="ERR 002" # Bad request syntax used with a known command
ERR_INVALID_MODULE       ="ERR 003" # Invalid or missing module and/or connector address
ERR_NO_CR                ="ERR 004" # No carriage return found.
ERR_NOT_SUPPORTED        ="ERR 005" # Command not supported by current Flex Link Port setting.
ERR_SETTINGS_LOCKED      ="ERR_006" # Settings are locked

# serial errors
ERR_INVALID_BAUD_RATE    ="ERR SL001" # Invalid baud rate
ERR_INVALID_FLOW_SETTING ="ERR SL002" # Invalid flow control or duplex setting
ERR_INVALID_PARITY       ="ERR SL003" # Invalid parity setting
ERR_INVALID_STOP_BITS    ="ERR SL004" # Invalid stop bits setting

class iTachCommandTCPRequestHandler(socketserver.BaseRequestHandler):
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
            log.ERROR("Unknown request: {self._data}")

    def send_response(self, response):
        log.INFO("Sending response: %s", response)
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
        # the iTach Flex host network module address is always hardcoded 0:1
        #   NET,0:1,<configlock>,<ipsetting>,<ipaddress>,<subnet>,<gateway>
#        if !self._data.startsWith("get_NET,0:1"):
#            throw error
        self.send_response("NET,0:1,LOCKED,STATIC,127.0.0.1,255.255.255.0,127.0.0.1")

    def handle_get_SERIAL(self):
        m = re.search("get_SERIAL,1:(?P<port>.+)", self._data)
        if m:
            port = int(m.group('port'))

            serial = config['serial']['port']
            if serial:
                self.send_response(f"SERIAL,1:{port},{serial['baud']},{serial['flow']},{serial['parity']},{serial['stop_bits']}")

            else:
                send_error()

    def handle_set_SERIAL(self):
        # FIXME: do we update the in-memory config!?  Or just disable setting serial configuration?

        # set_SERIAL,<module>:<port>
        # set_SERIAL,<module>:<port>,<baudrate>,<flowcontrol/duplex>,<parity>,[stopbits]

        # response: SERIAL,1:1,<baudrate>,<flowcontrol/duplex>,<parity>,<stopbits>
        self.send_response("SERIAL,1:1,115200,FLOW_NONE,PARITY_NO,STOPBITS_1")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

# listener that relays data to/from a specific RS232 port
# ... we only allow a single client to connect to the TCP for a serial
class RS232SerialTCPServer(socketserver.TCPServer):
    def __init__(self, serial_path):
        self._serial_path = serial_path
        # FIXME: open serial connection

    def handle(self):
        self._data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self._data)


@app.route('/')
def web_console():
    return '<h1>Virtual iTach Flex Serial Console</h1>'

def start_command_listener():
    server = ThreadedTCPServer(("localhost", ITACH_FLEX_COMMAND_TCP_PORT), iTachCommandTCPRequestHandler)

    # start a thread with the server -- that thread will start a new thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True # exit the server thread when the main thread terminates
    server_thread.start()

    # FIXME: should we limit the maximum threads that can be created (e.g. max simultaneous clients)
    # server.serve_forever()

    server.shutdown()
    server.server_close()

def read_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            sys.stderr.write(f"FATAL! {exc}")
            sys.exit(1)

config = read_config("config/ports.yaml")

def main():
    beacon = HeartbeatBeacon(config)

    start_command_listener()

    port = 4999
    for serial_config in config['serial']:
        log.info("Found serial config for %s", serial_config)

    # run the Flask http console server in the main thread
    app.run(debug=True, host='127.0.0.1', port='8080') # FIXME: allow env override, but default to 80!


if __name__ == '__main__':
  main()
