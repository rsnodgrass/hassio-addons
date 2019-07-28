#!/usr/local/bin/python3
#
# Emulates a Global Cache iTach Flex IP2SL (IP to Serial) to provide bidirectional
# TCP-to-serial connections to physical serial ports connected to the host running
# this microservice. Up to eight physical RS232/RS485 serial ports can be exposed
# through the TCP API by each running instance of this Virtual Adapter.

import logging
from flask import Flask

import os
import re
import sys
import uuid
import time
import yaml

import atexit
import threading
import socket
import socketserver

import logging
import logging.config
import server

from beacon import AMXDiscoveryBeacon
from listener import start_serial_listeners

log = logging.getLogger(__name__)

FLEX_TCP_API_VERSION = '1.6'
FLEX_COMMAND_TCP_PORT = 4998

app = Flask(__name__)

# general errors
ERR_INVALID_REQUEST      ="ERR 001"   # Invalid request. Command not found.
ERR_INVALID_SYNTAX       ="ERR 002"   # Bad request syntax used with a known command
ERR_INVALID_MODULE       ="ERR 003"   # Invalid or missing module and/or connector address
ERR_NO_CR                ="ERR 004"   # No carriage return found.
ERR_NOT_SUPPORTED        ="ERR 005"   # Command not supported by current Flex Link Port setting.
ERR_SETTINGS_LOCKED      ="ERR_006"   # Settings are locked

# serial errors
ERR_INVALID_BAUD_RATE    ="ERR SL001" # Invalid baud rate
ERR_INVALID_FLOW_SETTING ="ERR SL002" # Invalid flow control or duplex setting
ERR_INVALID_PARITY       ="ERR SL003" # Invalid parity setting
ERR_INVALID_STOP_BITS    ="ERR SL004" # Invalid stop bits setting

Valid_Config_Values = {
#    "baud": [] # 300|…|115200
    "flow":     [ 'FLOW_HARDWARE', 'FLOW_NONE', 'DUPLEX_HALF', 'DUPLEX_FULL' ],
    "parity":   [ 'PARITY_NO', 'PARITY_ODD', 'PARITY_EVEN' ],
    "stopbits": [ 'STOPBITS_1', 'STOPBITS_2' ] # optional
}

def read_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            sys.stderr.write(f"FATAL! {exc}")
            sys.exit(1)

config = read_config("config/ports.yaml")

def setup_logging(
    default_path='config/logging.yaml',
    default_level=logging.INFO,
    env_key='LOG_CONFIG'
):
    """Setup logging configuration"""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

        log = logging.getLogger(__name__)
        log.debug("Read logging configuration from %s: %s", path, config)
    else:
        print(f"ERROR! Couldn't find logging configuration: {path}")
        logging.basicConfig(level=default_level)

setup_logging()
log = logging.getLogger(__name__)

class iTachCommandTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self._data = self.request.recv(1024).strip()
        print(f"{self.client_address[0]} wrote: {self._data}")
        log.debug(f"{self.client_address[0]} wrote: %s", self._data)

        if self._data == b"getdevices":
            self.handle_getdevices()
        elif self._data == b"getversion":
            self.handle_getversion()
        elif self._data.startsWith("get_NET"):
            self.handle_get_NET()
        elif self._data.startsWith("get_SERIAL"):
            self.handle_get_SERIAL()
        elif self._data.startsWith("set_SERIAL"):
            self.handle_set_SERIAL()
        else:
            log.error("Unknown request: {self._data}")

    def send_response(self, response):
        log.info("Sending response: %s", response)
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


@app.route('/')
def web_console():
    return '<h1>Virtual iTach Flex Serial Console</h1>'

@atexit.register
def shutdown_listeners():
    log.info("Atexit handler shutdown_listeners()")
    #shutdown_all_listeners()
    #command_server.shutdown()
    #command_server.server_close()

def start_command_listener():
    host = os.getenv('FLEX_SERVER_IP', '0.0.0.0')

    log.info(f"Starting Flex TCP API command listener at {host}:{FLEX_COMMAND_TCP_PORT}")
    print(f"Starting Flex TCP API command listener at {host}:{FLEX_COMMAND_TCP_PORT}")
    server = ThreadedTCPServer((host, FLEX_COMMAND_TCP_PORT), iTachCommandTCPRequestHandler)

    # the command listener is in its own thread which then creates a new thread for each TCP request
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True # exit the server thread when the main thread terminates
    server_thread.start()

    # FIXME: do we need ot shutdown the server cleanly on exit?
    # server.shutdown()
    # server.server_close()


def main():
    beacon = AMXDiscoveryBeacon(config)
    start_command_listener()
    start_serial_listeners(config)

    host = os.getenv('FLEX_SERVER_IP', '0.0.0.0')

    # run the http console server in the main thread
    console_port = 4444
    log.info(f"Starting UI console at http://{host}:{console_port}")
    print(f"Starting UI console at http://{host}:{console_port}")
    app.run(debug=True, host=host, port=console_port) # FIXME: allow env override, but default to 80!

if __name__ == '__main__':
  main()
