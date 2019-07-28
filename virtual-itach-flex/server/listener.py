import logging

import time
import threading
import socketserver

log = logging.getLogger(__name__)

ITACH_FLEX_SERIAL_TCP_PORT_START = 4999
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
multiplexed, we only allow a single instance of this instantiated at a time
(this is the default behavior with out we've constructed the threading model).
"""
class SerialTCPHandler(socketserver.BaseRequestHandler):
#    def __init__(self, config, virtual_port):
#        self._config = config
#        self._port = virtual_port

    def handle(self):
        self._data = self.request.recv(1024).strip()
        print(f"{self.client_address[0]} wrote: {self._data}")
        log.debug(f"{self.client_address[0]} wrote: %s", self._data)

# self.request.sendall(self.data.upper())

def start_serial_listeners(config):

    # start the individual TCP ports for each serial port

    log.info("Starting serial port TCP listeners")
    host = "localhost"
    port = ITACH_FLEX_SERIAL_TCP_PORT_START

    for serial_config in config['serial']:
        log.info("Found serial config: %s (port %d)", serial_config, port)
        server = socketserver.TCPServer((host, port), SerialTCPHandler)

        # each listener has a dedicated thread (one thread per port, as serial port communication isn't multiplexed)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True # exit the server thread when the main thread terminates

        log.info(f"Starting Flex TCP listener on %s:%d", host, port)
        server_thread.start()

        # retain references to the thread and server
        serial_listeners.append( server )
        port += 1
