import logging

import os
import time
import serial
import threading
import socketserver

import util
import ip2serial

log = logging.getLogger(__name__)

Serial_Listeners = {}

# initialize the map of serial port number to TCP port; we only limit to 8 ports
# since existing hardware which implements the Flex command protocol isn't found
# in sizes larger than 8 ports, so unclear what client behavior would be.
SERIAL_PORT_TO_TCP_PORT = { 8: 5007 }
def initialize_serial_port_to_tcp_port():
    num_ports = 8
    for i in range(1, num_ports):
        SERIAL_PORT_TO_TCP_PORT[i] = 4998 + i
initialize_serial_port_to_tcp_port()

""" 
Listener that relays data to/from a specific serial port. This is instantiated
once per connection to the server.  Since the serial port communication is not
multiplexed, only allow a single instance of this instantiated at a time
(this is the default behavior given the current threading model).
"""
class IPToSerialTCPHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, what_self):
        print(f"Connecting to serial ...")

    def handle(self):
        with self.server._lock:
             data = self.request.recv(1024).strip()
             print(f"{self.client_address[0]} wrote: {data}")
             log.debug(f"{self.client_address[0]} wrote: %s", data)

    #        self.server._serial = self.server._serial

    def update_serial(new_config):
        with self.server._lock:
           self.server._serial.reset_serial_parameters(new_config)


class IP2SLServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, serial_connection):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
        
        self._serial = serial_connection

        # each listener has a lock, since the main control thread can modify
        # parameters for the serial connetion such as baud rate. We do not want
        # one large lock shared across listeners since then that serializes the
        # processing for all threads.
        self._lock = threading.Lock()


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

def start_listener(config, port_number, serial_config):
    host = util.get_host(config)
    tcp_port = SERIAL_PORT_TO_TCP_PORT[port_number]

    log.info(f"Serial {port_number} configuration: {serial_config} (TCP port {host}:{tcp_port})")
    serial_connection = ip2serial.IP2SLSerialInterface(serial_config)
    # FIXME: if serial port /dev/tty does not exist, should port be opened?

    server = IP2SLServer((host, tcp_port), IPToSerialTCPHandler, serial_connection)

    # each listener has a dedicated thread (one thread per port, as serial port communication isn't multiplexed)        
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True # exit the server thread when the main thread terminates

    log.info(f"Starting raw IP-to-serial TCP listener at {host}:{tcp_port}")
    server_thread.start()

    # retain references to the thread and server
    Serial_Listeners[port_number] = ( server )
    return server

def start_serial_listeners(config):
    # start the individual TCP ports for each serial port
    for port_number, serial_config in config['serial'].items():
        start_listener(config, port_number, serial_config)
