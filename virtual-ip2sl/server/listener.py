import logging

import os
import time
import serial
import threading
import socketserver

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
        self._serial = serial

    def handle(self):
        data = self.request.recv(1024).strip()
        print(f"{self.client_address[0]} wrote: {data}")
        log.debug(f"{self.client_address[0]} wrote: %s", data)

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
    # if existing listener for this port number is running, close it and kill the thread;
    # this should only happen when the listener/serial connection is reconfigured
    if port_number in Serial_Listeners:
       stop_listener(port_number)

    host = os.getenv('IP2SL_SERVER_HOST', '0.0.0.0') # FIXME: and from config!
    tcp_port = SERIAL_PORT_TO_TCP_PORT[port_number]

    log.info(f"Serial {port_number} configuration: {serial_config} (TCP port {tcp_port})")

    serial_connection = serial.IP2SLSerialInterface(serial_config)
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
