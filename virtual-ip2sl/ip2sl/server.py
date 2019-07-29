#!/usr/local/bin/python3
#
# Emulates a Global Cache iTach Flex IP2SL (IP to Serial) to provide bidirectional
# TCP-to-serial connections to physical serial ports connected to the host running
# this microservice. Up to eight physical RS232/RS485 serial ports can be exposed
# through the TCP API by each running instance of this Virtual Adapter.

import logging
from flask import Flask

import re

import atexit
import threading
import socket
import socketserver

import beacon
import util
from listener import start_serial_listeners

log = logging.getLogger(__name__)

FLEX_TCP_API_VERSION = '1.6'
FLEX_COMMAND_TCP_PORT = 4998

app = Flask(__name__)

threads = []

# general errors
ERR_INVALID_REQUEST      ='ERR 001'   # Invalid request. Command not found.
ERR_INVALID_SYNTAX       ='ERR 002'   # Bad request syntax used with a known command
ERR_INVALID_MODULE       ='ERR 003'   # Invalid or missing module and/or connector address
ERR_NO_CR                ='ERR 004'   # No carriage return found.
ERR_NOT_SUPPORTED        ='ERR 005'   # Command not supported by current Flex Link Port setting.
ERR_SETTINGS_LOCKED      ='ERR_006'   # Settings are locked

# serial errors
ERR_INVALID_BAUD_RATE    ='ERR SL001' # Invalid baud rate
ERR_INVALID_FLOW_SETTING ='ERR SL002' # Invalid flow control or duplex setting
ERR_INVALID_PARITY       ='ERR SL003' # Invalid parity setting
ERR_INVALID_STOP_BITS    ='ERR SL004' # Invalid stop bits setting

util.setup_logging()
log = logging.getLogger(__name__)

config = util.read_config()

class FlexCommandTCPHandler(socketserver.BaseRequestHandler):
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
        # the Flex host network module address is always hardcoded 0:1
        #   NET,0:1,<configlock>,<ipsetting>,<ipaddress>,<subnet>,<gateway>
#        if !self._data.startsWith("get_NET,0:1"):
#            throw error
        # FIXME: can we just ignore this API?
        self.send_response("NET,0:1,LOCKED,STATIC,127.0.0.1,255.255.255.0,127.0.0.1")

    # response: SERIAL,1:1,<baudrate>,<flowcontrol/duplex>,<parity>,<stopbits>
    def _prepare_SERIAL_response(self):
        m = re.search("et_SERIAL,1:(?P<port>.+)", self._data)
        if m:
            port = int(m.group('port'))

            # FIXME: actually get this form the serial object (since it could have changed)
            cfg = config['serial']['port']
            if cfg:
                return f"SERIAL,1:{port},{cfg['baud']},{cfg['flow']},{cfg['parity']},{cfg['stop_bits']}"
            return None # FIXME
   
    def handle_get_SERIAL(self):
        response = self._prepare_SERIAL_response()
        self.send_response(response)

    def handle_set_SERIAL(self):
        # FIXME: do we update the in-memory config!?  Or just disable setting serial configuration?
        # FIXME: should we persist this across restarts?
        
        # set_SERIAL,<module>:<port>
        # set_SERIAL,<module>:<port>,<baudrate>,<flowcontrol/duplex>,<parity>,[stopbits]
        response = self._prepare_SERIAL_response()

        # FIXME: partial search of stopbits!
        m = re.search("set_SERIAL,1:(?P<port>.+),(?P<baud>.+),(?P<flow>.+),(?P<parity>.+),(?P<stop_bits>.+)", self._data)
        if m:
            cfg = config['serial']['port']
            if cfg:
                cfg['baud'] = int(m.group('baud'))
                cfg['parity'] = m.group('parity')
                # FIXME: flow!
                cfg['stop_bits'] = m.group('stop_bits')

                # FIXME: find the listener/serial, close it, and recreate a new one (treat as immutable)

                # FIXME: find the serial port that matches, and update
                #self._serial.reset_configuration(cfg) # FIXME
            else:
                log.error(f"Major set_SERIAL error! Could not parse: {self._data}")
                # FIXME: return error
 
        # always reply with the current configuration
        response = self._prepare_SERIAL_response()
        self.send_response(response)
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

@app.route('/')
def web_console():
    return '<h1>Virtual iTach Flex Serial Console</h1>'

@atexit.register
def shutdown_listeners():
    log.info("Atexit handler shutdown_listeners()")
    #stop_all_listeners()
    #command_server.shutdown()
    #command_server.server_close()

def start_command_listener():
    host = util.get_host(config)

    log.info(f"Starting Flex TCP command listener at {host}:{FLEX_COMMAND_TCP_PORT}")
    print(f"Starting Flex TCP command listener at {host}:{FLEX_COMMAND_TCP_PORT}")
    server = ThreadedTCPServer((host, FLEX_COMMAND_TCP_PORT), FlexCommandTCPHandler)

    # the command listener is in its own thread which then creates a new thread for each TCP request
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True # exit the server thread when the main thread terminates
    server_thread.start()

    threads.append(server_thread)

def main():
    ip2sl_beacon = beacon.AMXDiscoveryBeacon(config)

    start_serial_listeners(config)
    start_command_listener()

    # until Flask http bind issue is resolved, just wait for all threads to complete before exiting
    for a_thread in threads:
        a_thread.join()
    exit

    # run the http console server in the main thread
    host = util.get_host(config)
    console_port = 4444

    log.info(f"Starting UI console at http://{host}:{console_port}")
    print(f"Starting UI console at http://{host}:{console_port}")
    app.run(debug=True, host=host, port=console_port) # FIXME: allow env override, but default to 80!

if __name__ == '__main__':
  main()
