import logging

import os
import time
import threading
import socketserver

log = logging.getLogger(__name__)

IP2SL_SERIAL_TCP_PORT_START = 4999
serial_listeners = []

Valid_Config_Values = {
#    "baud": [] # 300|…|115200
    "flow":     [ 'FLOW_HARDWARE', 'FLOW_NONE', 'DUPLEX_HALF', 'DUPLEX_FULL' ],
    "parity":   [ 'PARITY_NO', 'PARITY_ODD', 'PARITY_EVEN' ],
    "stopbits": [ 'STOPBITS_1', 'STOPBITS_2' ] # optional
}

""" 
Listener that relays data to/from a specific serial port. This is instantiated
once per connection to the server.  Since the serial port communication is not
multiplexed, only allow a single instance of this instantiated at a time
(this is the default behavior given the current threading model).
"""
class IPToSerialTCPHandler(socketserver.BaseRequestHandler):
#    def __init__(self, config, virtual_port):
#        self._config = config
#        self._port = virtual_port

    def handle(self):
        data = self.request.recv(1024).strip()
        print(f"{self.client_address[0]} wrote: {data}")
        log.debug(f"{self.client_address[0]} wrote: %s", data)

# self.request.sendall(self.data.upper())

"""Ensure all listeners are cleanly shutdown"""
def shutdown_all_listeners():
    for server in serial_listeners:
        server.shutdown()
        server.server_close()

def start_serial_listeners(config):
    host = os.getenv('IP2SL_SERVER_HOST', '0.0.0.0')
    tcp_port = IP2SL_SERIAL_TCP_PORT_START

    # start the individual TCP ports for each serial port
    for port_number, serial_config in config['serial'].items():
        log.info("Serial %d configuration: %s (port %d)", port_number, serial_config, tcp_port)
        server = socketserver.TCPServer((host, tcp_port), IPToSerialTCPHandler)

        # FIXME: if serial port /dev/tty does not exist, should port be opened?

        # each listener has a dedicated thread (one thread per port, as serial port communication isn't multiplexed)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True # exit the server thread when the main thread terminates

        log.info(f"Starting raw IP-to-serial TCP listener at {host}:{tcp_port}")
        print(f"Starting raw IP-to-serial TCP listener at {host}:{tcp_port}")
        server_thread.start()

        # retain references to the thread and server
        serial_listeners.append( server )
        tcp_port += 1