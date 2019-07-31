import logging

import os
import time
import serial
import threading
import socketserver

import util
import ip2serial

log = logging.getLogger(__name__)

# initialize the map of serial port number to TCP port; we only limit to 8 ports
# since existing hardware which implements the Flex command protocol isn't found
# in sizes larger than 8 ports, so unclear what client behavior would be.
SERIAL_PORT_TO_TCP_PORT = { 8: 5007 }
def initialize_serial_port_to_tcp_port():
    num_ports = 8
    for i in range(1, num_ports):
        SERIAL_PORT_TO_TCP_PORT[i] = 4998 + i
initialize_serial_port_to_tcp_port()

Serial_Proxies = {}
def get_serial_proxies():
    return Serial_Proxies

""" 
Handler that proxies data to/from a specific serial port to the connected TCP
connection. This is instantiated once per client connection.  Since the serial
port communication is not multiplexed, only allow a single instance of this
instantiated at a time (this is the default behavior given the current threading model).
"""
class TCPToSerialProxy(socketserver.StreamRequestHandler):
    def __init__(self, request, client_address, server):
        log.debug(f"New serial connection from %s: %s", client_address[0], {request})
        self._server = server

        # call the baseclass initializer as the last thing; note __init__ waits on bytes to call handle()
        socketserver.StreamRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        data = self.request.recv(1024).strip()
        log.debug(f"{self.client_address[0]} wrote to %s: %s", self._server._serial._tty_path, data)
        print(f"{self.client_address[0]} wrote to %s: %s", self._server._serial._tty_path, data)

        # FIXME: could we add MORE layers here :(
        # pass all bytes directly to the serial port
        self._server._serial._serial.write(data)

    def proxy_loop(self, server, serial):
        while True:
            r, w, e = select.select([client, serial], [], [])

            if client in r:
                data = client.recv(4096)
                log.debug("Proxying from %s to serial: %s", client_address[0], data)
                if serial.send(data) <= 0:
                        break

            # if data available from the serial port, read it and forward to TCP socket
            if serial in r:
                data = serial.recv(4096)
                log.debug("Proxying from serial to %s: %s", client_address[0], data)
                if client.send() <= 0:
                        break

class IP2SLServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, serial_connection):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
        
        self._serial = serial_connection

        # FIXME: NOT YET IMPLEMENTED
        # each listener has a lock, since the main control thread can modify
        # parameters for the serial connetion such as baud rate. We do not want
        # one large lock shared across listeners since then that serializes the
        # processing for all threads.
        self._lock = threading.Lock()

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

def start_proxy_listener(config, port_number, serial_config):
    host = util.get_host(config)
    tcp_port = SERIAL_PORT_TO_TCP_PORT[port_number]

    log.info(f"Serial {port_number} configuration: {serial_config} (TCP port {host}:{tcp_port})")
    serial_connection = ip2serial.IP2SLSerialInterface(serial_config)

    # FIXME: if serial port /dev/tty does not exist, should port be opened?

    IP2SLServer((host, tcp_port), TCPToSerialProxy, serial_connection)

    # each listener has a dedicated thread (one thread per port, as serial port communication isn't multiplexed)        
    log.info(f"Starting thread for TCP proxy to serial {port_number} at {host}:{tcp_port}")
    proxy_thread = threading.Thread(target=proxy.serve_forever)
    proxy_thread.daemon = True # exit the server thread when the main thread terminates
    proxy_thread.start()

    # retain references to the thread and proxy
    Serial_Proxies[port_number] = ( proxy )
    return proxy

def start_serial_proxies(config):
    # start the individual TCP listeners for each serial port proxy
    for port_number, serial_config in config['serial'].items():
        start_proxy_listener(config, port_number, serial_config)
        