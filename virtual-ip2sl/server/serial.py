# Common support functionality for RS232 serial connection including
# configuration and helper functions.

import sys
import time
import serial
import logging

log = logging.getLogger(__name__)

DEFAULT_TTY_TIMEOUT_SECONDS = 5

PARITY = {
    'PARITY_NO':   serial.PARITY_NONE,
    'PARITY_ODD':  serial.PARITY_ODD,
    'PARITY_EVEN': serial.PARITY_EVEN
}

STOP_BITS = {
    'STOPBITS_1':  serial.STOPBITS_ONE,
    'STOPBITS_2':  serial.STOPBITS_TWO
}

class SerialInterface:

    def __init__(self, config):
        self._tty_path = config['path']
        reset_serial_parameters(self, config)

    def serial(self):
        return self._serial

    def default(config, key, default):
        if key in config:
            return config[key]
        else:
            return default

    def reset_serial_parameters(self, config):
        try:
            # if serial port is already opened, then close before reconfiguring
            if self._serial:
                self._serial.close()

            baud = int(default(config, 'baud', 9600))
            self._baud = max(min(baud, 115200), 300) # ensure baud is ranged between 300-115200

            self._parity    = PARITY[default(config, 'parity', 'PARITY_NO')]
            self._stop_bits = STOP_BITS[default(config, 'stop_bits', 'STOPBITS_1')]
            self._timeout   = int( default(config, 'timeout', DEFAULT_TTY_TIMEOUT_SECONDS) )
            
            # default to hardware flow control on (FLOW_HARDWARE)
            flow_rtscts = True
            flow_dsrdtr = True
            if self._flow == 'FLOW_NONE':
                flow_rtscts = False
                flow_dsrdtr = False

            self._serial = serial.Serial(self._tty_path,
                                         timeout=self._timeout,
                                         baudrate=self._baud,
                                         parity=self._parity,
                                         stopbits=self._stop_bits,
                                         bytesize=serial.EIGHTBITS,
                                         dsrdtr=flow_dsrdtr,
                                         rtscts=flow_rtscts)
            log.info(f"Connected to {self._tty_path} (baud rate={self._baud}; timeout={self._timeout})")

            self._rs485 = self._flow in [ 'DUPLEX_FULL', 'DUPLEX_HALF' ]
            if self._rs485:
                message = f"RS485 communication not yet supported! (detected RS485 flow/duplex {self._flow} configuration)"
                log.error(message)
                raise RuntimeError(message)
                # FIXME: support RS485
                #   ser.rs485_mode = serial.rs485.RS485Settings()

        except:
            log.error("Unexpected error: %s", sys.exc_info()[0])
            raise RuntimeError("Connect failure to {}".format(self._tty))