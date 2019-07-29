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


PARITY = {
    'PARITY_NO': serial.PARITY_NONE,
    'PARITY_ODD': serial.PARITY_ODD,
    'PARITY_EVEN': serial.PARITY_EVEN
}

FLOW = {
    'FLOW_HARDWARE':
    'FLOW_NONE':
    'DUPLEX_HALF':
    'DUPLEX_FULL':
}

STOP_BITS = {
    'STOPBITS_1': serial.STOPBITS_ONE,
    'STOPBITS_2': serial.STOPBITS_TWO
}

class SerialInterface:

    def __init__(self, config):
        try:
            self._tty_path  = config['path']

            # ensure baud is ranged between 300-115200
            self._baud = max(min(config['baud'], 115200), 300)
           
            self._flow      = FLOW[config['flow']]
            self._parity    = PARITY[config['parity']]
            self._stop_bits = STOP_BITS[config['stop_bits']]
            self._timeout   = DEFAULT_TTY_TIMEOUT_SECONDS  #int(config['timeout'])

            # default to hardware flow control on (FLOW_HARDWARE)
            flow_rtscts = True
            flow_dsrdtr = True
            if self._flow == 'FLOW_NONE':
                flow_rtscts = False
                flow_dsrdtr = False

            self._serial = serial.Serial(self._tty,
                                         timeout=self._timeout,
                                         baudrate=self._baud,
                                         parity=self._parity,
                                         stopbits=self._stop_bits,
                                         bytesize=serial.EIGHTBITS,
                                         dsrdtr=flow_dsrdtr,
                                         rtscts=flow_rtscts)
            log.info(f"Connected to {self._tty,} (baud rate={self._baud}; timeout={self._timeout})")

            self._rs485 = self._flow in [ 'DUPLEX_FULL', 'DUPLEX_HALF' ]
            if self._rs485:
                message = f"RS485 communication note yet supported!  RS485 flow/duplex {self._flow} specified."
                log.error(message)
                raise RuntimeError(message)
                # FIXME: add more settings!
                #              ser.rs485_mode = serial.rs485.RS485Settings(

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
