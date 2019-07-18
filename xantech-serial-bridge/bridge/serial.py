# Bridge to RS232 serial connection including configuration support and
# helper functions. This can be shared between multiple bridges so should
# not contain any hardware specific details.

import os
import sys
import time
import serial
import logging

log = logging.getLogger(__name__)

DEFAULT_TTY = '/dev/ttyUSB0'
DEFAULT_TTY_TIMEOUT = 1
DEFAULT_BAUD_RATE = 9600
DEFAULT_NEWLINE = '\r'

EXAMPLE_TTY_PATHS = [
    '/dev/ttyS0',         # Raspberry Pi mini UART GPIO
    '/dev/ttyAMA0',       # Raspberry Pi GPIO pins 14/15 (pre-Bluetooth RPi 3)
    '/dev/serial0',       # RPi 3 serial port alias 1
    '/dev/serial1',       # RPi 3 serial port alias 2
    '/dev/tty.usbserial', # typical MacOS USB serial adapter
    '/dev/ttyUSB0',       # Linux USB serial 1
    '/dev/ttyUSB1',       # Linux USB serial 2
    '/dev/ttyUSB2'        # Linux USB serial 3
]

#def get_env_value(envname, default):
#    if envname in os.environ:
#        return os.getenv(envname)
#    return default

class BridgeSerial:

    def __init__(self):
        try:
            self._tty      = os.getenv('BRIDGE_TTY', DEFAULT_TTY)
            self._timeout  = int(os.getenv('BRIDGE_TTY_TIMEOUT', DEFAULT_TTY_TIMEOUT))
            self._baud     = int(os.getenv('BRIDGE_BAUD_RATE', DEFAULT_BAUD_RATE))
            self._newline  = os.getenv('BRIDGE_NEWLINE', DEFAULT_NEWLINE)
            self._encoding = 'utf-8'

            self._serial   = serial.Serial(self._tty, timeout=self._timeout, baudrate=self._baud_rate,
                                           parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                                           bytesize=serial.EIGHTBITS, dsrdtr=True, rtscts=True)

            # NOTE: according to Monoprice RS232 Control Codes manual, it appears that the serial
            # baud rate defaults to 9600, but then can be reconfigured (until next time power is
            # lost to the amplifier) up to 230400 baud!

        except:
            log.error("Unexpected error: %s", sys.exc_info()[0])
            raise RuntimeError("Connect failure to {}".format(self._tty))

    # not efficient reading one byte at a time, but way faster than waiting
    # for 1+ second timeout on every read.
    # FIXME: This *SHOULD* be improved in future.
    def _readline(self):
        eol = b'\r'
        leneol = len(eol)
        line = bytearray()
        while True:
            c = self._serial.read(1)
            if c:
                if c == eol:
                    break
                line += c
            else:
               break
        return bytes(line).decode(self._encoding)

    def write_command(self, data):
        log.debug('>>> Serial write: {}'.format(data))
        self._serial.reset_input_buffer()
        output = (data + self._newline).encode(self._encoding)
        self._serial.write(output)

    def read_line(self):
        start = time.time()

        raw_data = self._readline()
        result = raw_data.decode('utf-8')
        end = time.time()

        log.debug('>>> Serial read ({1:.0f} ms): {0}'.format(result, 1000 * (end-start)))
        return result

    # read all lines of data available until none more available
    def read_lines(self):
        start = time.time()

        raw_data = self._readline()
        while self._serial.in_waiting:
            raw_data += self._readline()
        result = raw_data.decode('utf-8')

        end = time.time()
        log.debug('>>> Serial read ({1:.0f} ms): {0}'.format(result, 1000 * (end-start)))
        return result