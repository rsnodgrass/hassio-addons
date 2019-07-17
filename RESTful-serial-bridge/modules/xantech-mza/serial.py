# Serial support for Xantech's Multi-Zone matrix audio RS232 protocol.
#
# NOTE: The Monoprice multi-zone amps share a variation of the same protocol as Xantech, and are likely
# licensed (or acquired) from Xantech since they no longer produce multi-zone amplifiers/controllers.
# Monoprice versions has a "channel" concept, into true matrix switching, with selection for each zone
# of either LINE or BUS. Also Monoprice supports chaining together up to 2 additional amps (as slaves),
# with the the NodeJS 6zhmaut API writing "?10\r" if single zone, followed by "?20\r" (if 2), and then
# "?30\r" (if 3) upon startup of the server. 
#       See: https://downloads.monoprice.com/files/manuals/31028_Manual_180731.pdf
#
# FIXME:
# - Determining what features are supported by doing a zone status query for zone 1,
#   depending on what it returns indicates the feature set
#      - source select (matrix) vs channel select (simple switching)
#      - number of zones
#      - number of sources
#
# Xantech firmware release notes make some mention of RS232 feature changes:
#   https://www.xantech.com/firmware-updates

import logging

log = logging.getLogger(__name__)

class XantechSerial:
    def __init__(self):
        self._name = 'Xantech'

        self._max_zones = 8
        self._zone_map = {}

        self._max_sources = 8
        self._source_map = {}

        self._serial = self.initializeConnection()
        self.initializeDevice()

    def initializeConnection():
        #    serial "/dev/ttyUSB0";
        # Monoprice baudrate: 9600
        # Xantech baudrate: 9600, though some docs suggest 19200 or 38400
        return

    def initializeDevice():
        # FIXME: should we disable state publishing automatically?
        #self.writeCommand("!ZA0+") # disable activity notifications (0 = true)
        #self.writeCommand("!ZP0+") # disable period auto updates (seconds = 0)
        return

    def write(string):
        return self._serial.writeCommand(string)
    
    def read(string):
        return self._serial.readData(string)

    # the input string should have {} as the substitution token for the zone_id
    def writeToAllZones(string):
        for zone_id in range(8):
            write(string.format(zone_id))

    def isValidZone(zone_id):
        if zone_id <= 0:
            return False
        elif zone_id > self._max_zones:
            # FIXME: determine if valid based on configuration for amplifier (model, number of slaves, etc)
            return False
        return True

    def isValidSource(source_id):
        if source_id <= 0:
            return False
        elif source_id > self._source_zones:
            # FIXME: determine if valid based on configuration for amplifier
            return False
        return True