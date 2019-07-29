# Common support functionality for RS232 serial connection including
# configuration and helper functions.

import sys
import time
import serial
import logging
import threading

log = logging.getLogger(__name__)

DEFAULT_TTY_TIMEOUT_SECONDS = 5

DEFAULT_CONFIG = {
    'baud':      '9600',
    'flow':      'FLOW_NONE',
    'parity':    'PARITY_NO',
    'stop_bits': 'STOPBITS_1'
}

PARITY = {
    'PARITY_NO':   'N', # serial.PARITY_NONE,
    'PARITY_ODD':  'O', # serial.PARITY_ODD,
    'PARITY_EVEN': 'E'  # serial.PARITY_EVEN
}

STOP_BITS = {
    'STOPBITS_1':  1, # serial.STOPBITS_ONE
    'STOPBITS_2':  2  # serial.STOPBITS_TWO
}

FLOW_OR_DUPLEX = {
    'FLOW_HARDWARE': 'rs232',
    'FLOW_NONE':     'rs232',
    'DUPLEX_HALF':   'rs485',
    'DUPLEX_FULL':   'rs485'
}

def DEFAULT(config, key, default):
    if key in config:
        return config[key]
    else:
        return default

class IP2SLSerialInterface:
    def __init__(self, config):
        self._lock = threading.Lock()
        self._tty_path = config['path']

        try:
            self._config = config

            baud = int(DEFAULT(config, 'baud', 9600))
            self._baud = max(min(baud, 115200), 300) # ensure baud is ranged between 300-115200
            config['baud'] = self._baud # rewrite config to ensure it is within range

            self._parity    = PARITY[DEFAULT(config, 'parity', 'PARITY_NO')]
            self._stop_bits = STOP_BITS[DEFAULT(config, 'stop_bits', 'STOPBITS_1')]
            self._timeout   = int( DEFAULT(config, 'timeout', DEFAULT_TTY_TIMEOUT_SECONDS) )
            
            # default to hardware flow control on (FLOW_HARDWARE)
            self._flow  = DEFAULT(config, 'flow', 'FLOW_HARDWARE')
            flow_rtscts = (self._flow == 'FLOW_HARDWARE')
            flow_dsrdtr = flow_rtscts

            self._serial = serial.Serial(self._tty_path,
                                         timeout=self._timeout,
                                         baudrate=self._baud,
                                         parity=self._parity,
                                         stopbits=self._stop_bits,
                                         bytesize=serial.EIGHTBITS,
                                         dsrdtr=flow_dsrdtr,
                                         rtscts=flow_rtscts)
            log.info(f"Connected to {self._tty_path} (config={self._config})")
            print(f"Connected to {self._tty_path} (config={self._config})")

            self._rs485 = self._flow in [ 'DUPLEX_FULL', 'DUPLEX_HALF' ]
            if self._rs485:
                message = f"RS485 communication not yet supported! (detected RS485 flow/duplex {self._flow} configuration)"
                log.error(message)
                raise RuntimeError(message)
                # FIXME: support RS485
                #   ser.rs485_mode = serial.rs485.RS485Settings()

        except:
            log.error("Unexpected error: %s", sys.exc_info()[0])
            raise RuntimeError("Connect failure to {}".format(self._tty_path))

    def config(self):
        with self._lock:
            return self._config

    def close(self):
        with self._lock:
            self._serial.flush()
            self._serial.close()

#    def read():
#        with self._lock:

    def reset_serial_parameters(self, config):
        with self._lock:
            self._reset_serial_parameters(config)

    def _reset_serial_paramters(self, config):
        try:
            self._config = config

            baud = int(DEFAULT(config, 'baud', 9600))
            self._baud = max(min(baud, 115200), 300) # ensure baud is ranged between 300-115200
            config['baud'] = self._baud # rewrite config to ensure it is within range

            self._parity    = PARITY[DEFAULT(config, 'parity', 'PARITY_NO')]
            self._stop_bits = STOP_BITS[DEFAULT(config, 'stop_bits', 'STOPBITS_1')]
            self._timeout   = int( DEFAULT(config, 'timeout', DEFAULT_TTY_TIMEOUT_SECONDS) )
            
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
            log.info(f"Connected to {self._tty_path} (config={self._config})")
            print(f"Connected to {self._tty_path} (config={self._config})")

            self._rs485 = self._flow in [ 'DUPLEX_FULL', 'DUPLEX_HALF' ]
            if self._rs485:
                message = f"RS485 communication not yet supported! (detected RS485 flow/duplex {self._flow} configuration)"
                log.error(message)
                raise RuntimeError(message)
                # FIXME: support RS485
                #   ser.rs485_mode = serial.rs485.RS485Settings()

        except:
            log.error("Unexpected error: %s", sys.exc_info()[0])
            raise RuntimeError("Connect failure to {}".format(self._tty_))