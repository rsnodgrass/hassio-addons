import logging

import threading
import socket
import socketserver

import logging

log = logging.getLogger(__name__)

ITACH_FLEX_SERIAL_TCP_PORT_START = 4999

Valid_Config_Values = {
#    "baud": [] # 300|…|115200
    "flow":     [ 'FLOW_HARDWARE', 'FLOW_NONE', 'DUPLEX_HALF', 'DUPLEX_FULL' ],
    "parity":   [ 'PARITY_NO', 'PARITY_ODD', 'PARITY_EVEN' ],
    "stopbits": [ 'STOPBITS_1', 'STOPBITS_2' ] # optional
}

# listener that relays data to/from a specific RS232 port
# ... we only allow a single client to connect to the TCP for a serial
class SerialTCPRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, config, virtual_port):
        self._config = config
        self._port = virtual_port

    def handle(self):
        self._data = self.request.recv(1024).strip()
        print(f"{self.client_address[0]} wrote: {self._data}")
        log.debug(f"{self.client_address[0]} wrote: %s", self._data)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def start_serial_listeners(config):

    # start the individual TCP ports for each serial port
    port = ITACH_FLEX_SERIAL_TCP_PORT_START
    serial_listeners = []
    

    log.info("Starting serial port TCP listeners")
    
    for serial_config in config['serial']:
        log.info("Found serial config: %s (port %d)", serial_config, port)
        port += 1

        #server = ThreadedTCPServer(("localhost", port), SerialTCPRequestHandler)

        # start a thread with the server -- that thread will start a new thread for each request
        #server_thread = threading.Thread(target=server.serve_forever)
        #server_thread.daemon = True # exit the server thread when the main thread terminates
        #server_thread.start()

        #serial_listeners.append( server )

        # FIXME: should we limit the maximum threads that can be created (e.g. max simultaneous clients)