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

# FIXME: init raSerial
class XantechSerial:
    def initializeConnection():
        #    serial "/dev/ttyUSB0";
        # Monoprice baudrate: 9600
        # Xantech baudrate: 9600, though some docs suggest 19200 or 38400

    def initializeDevice():
        # FIXME: should we disable state publishing automatically?
        #raSerial.writeCommand("!ZA0+") # disable activity notifications (0 = true)
        #raSerial.writeCommand("!ZP0+") # disable period auto updates (seconds = 0)

    def write(string):
        return raSerial.writeCommand(string)
    
    def read(string):
        return raSerial.readData(string)

    # the input string should have {} as the substitution token for the zone_id
    def writeToAllZones(string):
        for zone_id in range(8):
            write(string.format(zone_id))

@ns.route('/power/on')
class XantechPowerOn(Resource):
    def get(self):
        raSerial.writeToAllZones("!{}PR1+")
        return {}

@ns.route('/power/off')
class XantechPowerOff(Resource):
    def get(self):
        # Xantech provides a special "All Zones Off" command instead of:
        #   raSerial.writeToAllZones("!{}PR0+")
        raSerial.writeCommand("!AO+")
        return {}

@ns.route('/mute/on')
class XantechPowerOn(Resource):
    def get(self):
        raSerial.writeToAllZones("!{}MU1+")
        return {}

@ns.route('/mute/off')
class XantechPowerOff(Resource):
    def get(self):
        raSerial.writeToAllZones("!{}MU0+")
        return {}
