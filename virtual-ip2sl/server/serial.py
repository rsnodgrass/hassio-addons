# Common support functionality for RS232 serial connection including
# configuration and helper functions.

import sys
import time
import serial
import logging

log = logging.getLogger(__name__)

DEFAULT_TTY = '/dev/ttyUSB0'
DEFAULT_TTY_TIMEOUT_SECONDS = 1
DEFAULT_BAUD_RATE = 9600

# FIXME: the constructor of this should pass in tty, timeouts, baud rate, since they
# should be configured on a per-interface level. Not ENV!

class BridgeSerial:

    def __init__(self, config, interface_slug):
        try:
            self._tty = config['tty']
            self._baud_rate = int(config['baud_rate'])
            self._timeout = DEFAULT_TTY_TIMEOUT_SECONDS  #int(config['timeout'])

            self._serial = serial.Serial(self._tty, timeout=self._timeout, baudrate=self._baud_rate,
                                         parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                                         bytesize=serial.EIGHTBITS, dsrdtr=True, rtscts=True)
            log.info("Connected to %s (baud rate=%d; timeout=%d)", self._tty, self._baud_rate, self._timeout)

        except:
            log.error("Unexpected error: %s", sys.exc_info()[0])
            raise RuntimeError("Connect failure to {}".format(self._tty))

    def raw_serial(self):
        return self._serial

    # not efficient reading one byte at a time, but way faster than waiting
    # for 1+ second timeout on every read.
    # FIXME: This *SHOULD* be improved!
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
