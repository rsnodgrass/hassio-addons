import logging

import os
import time
import serial
import threading
import socketserver

import ip2sl-serial

log = logging.getLogger(__name__)

SERIAL_PORT_TO_TCP_PORT = {
        1: 4999,
        2: 5000,
        3: 5001,
        4: 5002,
        5: 5003,
        6: 5004,
        7: 5005,
        8: 5006
}
Serial_Listeners = {}

""" 
Listener that relays data to/from a specific serial port. This is instantiated
once per connection to the server.  Since the serial port communication is not
multiplexed, only allow a single instance of this instantiated at a time
(this is the default behavior given the current threading model).
"""
class IPToSerialTCPHandler(socketserver.BaseRequestHandler):
    def __init(self, serial):
        # each listener has a lock, since the main control thread can modify
        # parameters for the serial connetion such as baud rate. We do not want
        # one large lock shared across listeners since then that serializes the
        # processing for all threads.
        self._lock = threading.Lock()

        self._serial = serial

    def handle(self):
        with self._lock:
             data = self.request.recv(1024).strip()
             print(f"{self.client_address[0]} wrote: {data}")
             log.debug(f"{self.client_address[0]} wrote: %s", data)

    def update_serial(new_config):
        with self._lock:
           self._serial.reset_serial_parameters(new_config)

# self.request.sendall(self.data.upper())

"""Ensure all listeners are cleanly shutdown"""
def stop_all_listeners():
    for port_number, server in Serial_Listeners.items():
        stop_listener(port_number)

def stop_listener(port_number):
    log.debug("Stopping listener for serial 1")
    server = Serial_Listeners[port_number]
    if server != None:
       server.shutdown()
       server.server_close()

def start_listener(port_number, serial_config):
    host = os.getenv('IP2SL_SERVER_HOST', '0.0.0.0') # FIXME: and from config!
    tcp_port = SERIAL_PORT_TO_TCP_PORT[port_number]

    log.info(f"Serial {port_number} configuration: {serial_config} (TCP port {tcp_port})")

    serial_connection = server.serial.IP2SLSerialInterface(serial_config)
    # FIXME: if serial port /dev/tty does not exist, should port be opened?

    server = socketserver.TCPServer((host, tcp_port),
                                    IPToSerialTCPHandler(serial_connection))

    # each listener has a dedicated thread (one thread per port, as serial port communication isn't multiplexed)        
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True # exit the server thread when the main thread terminates

    log.info(f"Starting raw IP-to-serial TCP listener at {host}:{tcp_port}")
    print(f"Starting raw IP-to-serial TCP listener at {host}:{tcp_port}")
    server_thread.start()

    # retain references to the thread and server
    Serial_Listeners[port_number] = ( server )
    return server

def start_serial_listeners(config):
    # start the individual TCP ports for each serial port
    for port_number, serial_config in config['serial'].items():
        start_listener(port_number, serial_config)
