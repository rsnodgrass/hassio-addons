# Bi-directional RS232 definitions for Xantech MRC88 interfaces.
#
# Not implemented:
#
# - explicitly setting bass/treble/balance...easy to add, but unclear if useful
#   except during initial amp setup, plus explicit lookup table values complex to document
# - current sense (audio) and video sense queries ... 12V?
#
# NOTE: The Monoprice multi-zone amps share a variation of the same protocol as Xantech, and are likely
# licensed (or acquired) from Xantech since they no longer produce multi-zone amplifiers/controllers.
#
# You may be able to determine what features are supported by doing a zone status query for zone 1,
# depending on what it returns indicates the feature set (e.g. source select vs channel select).
# Similarly, it may be possible to probe for maximum zones and sources without requiring config.
#
# MRAUDIO8X8
# MRAUDIO4x4

import os   
import json
import logging

from flask import request
from flask_restplus import Resource
#from bridge.api.manager.serializers import zone
from bridge.api.restplus import api

log = logging.getLogger(__name__)

UNKNOWN_NAME = "Unknown"

MinMaxValidation = {
    'zone': [1, 8],  # or 1..16 if expanded
    'source': [1, 8],
    'volume': [0, 38],
}

# FIXME: ensure amp isn't publishing back state except when requested:
# !ZA0+
# !ZP0+

# NOTE: this is very close to Monoprice!
#   except they have a "channel" concept!!  Even their docs are similar for RS232
#   ... AND they don't have multi-source multiplexing...(instead just LINE or BUS)...
#  https://downloads.monoprice.com/files/manuals/31028_Manual_180731.pdf

# FIXME: what must be configured
#  - for each zone, what zone type of switch/dimmer it is (default to dimmer)
#  - we should allow client to specify if they want ALL the zones (e.g. including Unassigned)

ns = api.namespace('zones', description='Zone operations')
raSerial = None

# FIXME: init raSerial
# FIXME: should this probe for versions/features/num zones/etc?
class XantechSerial:
    def write(string):
        return raSerial.writeCommand(string)
    
    def read(string):
        return raSerial.readData(string)

@ns.route('/')
class ZoneCollection(Resource):
    
    def _initialize_name_mapping(count, name_prefix):
        map = {}
        for i in 1 to count:
            map[i] = name_prefix + ' ' + i
        return map

    @api.marshal_list_with(zone)
    def get(self):
        max_zones = 8
        zone_map = _initialize_name_mapping("Zone", max_zones)

        max_sources = 8
        source_map = _initialize_name_mapping("Source", max_sources)
        source_map[1] = 'Sonos' # override

        details = {
            'module': 'xantech_mza',

            'max_zones': max_zones, # configurable
            'zones': { # configurable (could also have name maps)
                1: "Living Room",
                2: "Kitchen",
                3: "Master Bedroom",
                4: "Master Bathroom",
                5: "Office",
                6: "Basement",
                7: "Guest Bedroom",
                8: "Patio"
            },

            'max_sources': max_sources, # configurable
            'sources': source_map,
        } 

        return details

@ns.route('/<int:id>')
@api.response(404, 'Zone not found')
class ZoneState(Resource):

    #@api.marshal_with(zone)
    def get(self, zone_id):
        # FIXME: if zone < 0 or zone > 8, error state
        raSerial.writeCommand("?" + zone_id + "ZD+")

        # example Xantech response:
        #   #{z#}ZS PR{0/1} SS{s#} VO{v#} MU{0/1} TR{bt#} BS{bt#} BA{b#} LS{0/1} PS{0/1}+
        # example Monoprice response:
        #   #{z#}ZS VO{v#} PO{0/1} MU{0/1} IS{0/1}+
        response = raSerial.readData()

        state = {
            'zone': zone_id
        }

        for data in response.split():
            # verify the serial response matches the zone_id we just wrote data for
            if data[0] == '#':
                data_zone_id = int(data[1:][2])
                if data_zone_id != zone_id:
                    log.error("Unknown state! Request for zone %s returned state for zone %s: %s",
                              zone_id, data_zone_id, response)
                    return
                continue

            # for each type of data in the response, map into the state structure
            # (not all may be returned, depending on what features the amplifier supports)
            switch(data[0:2]) {
                case 'PR', 'PO': # Xantech / Monoprice
                    state['power'] = (data[3] == '1') # bool
                    break;
                case 'SS': # Xantech
                    state['source'] = int(data[3:])
                    break;
                case 'VO':
                    # map the 38 physical attenuation levels into 0-100%
                    attenuation_level = int(data[3:] 
                    state['volume'] = round(int(100 * attenuation_level) / 38))
                    break;
                case 'MU':
                    state['mute'] = (data[3] == '1') # bool
                    break;
                case 'TR':
                    state['treble'] = int(data[3:])
                    break;
                case 'BS':
                    state['bass'] = int(data[3:])
                    break;
                case 'BA':
                    state['balance'] = int(data[3:])
                    break;
                case 'LS': # Xantech
                    state['linked'] = (data[3] == '1') # bool
                    break;
                case 'PS': # Xantech
                    state['paged'] = (data[3] == '1') # bool
                    break;
                case 'IS': # Monoprice (audio input)
                    if data[3] == '1':
                        state['input'] = 'line'
                    else:
                        state['input'] = 'bus'
                    break;
                default:
                    log.error("Ignoring unknown state type %s found in: %s", data[0:2], response)
            }

        return state

####

# FIXME: I'm not sure we want REST Get with side effect, but it is very convenient!
# we could have gone all the way to 11, but instead decided on the range 0-100%
@ns.route('/<int:id>/volume/<int:percentage>')
class ZoneVolumeLevel(Resource):
    def post(self, zone_id, percentage):

        # While actual attenuation steps for Xantech is 0-38 (non-linearly from -78.75 db to 0 db),
        # for simplicity of API, we use range from 0-100% even though increase by 1%  <may not
        # necessarily change volume if it remains within the same dB attenuation step.
        attenuation_level = (38 * percentage) / 100
        raSerial.writeCommand("!" + zone_id + "VO" + attenuation_level + "+"
        return {}

@ns.route('/<int:id>/volume/up')
class ZoneVolumeUp(Resource):
    def post(self, zone_id):
        raSerial.writeCommand("!" + zone_id + "VI+")
        return {}

@ns.route('/<int:id>/volume/down')
class ZoneVolumeDown(Resource):
    def post(self, zone_id):
        raSerial.writeCommand("!" + zone_id + "VD+")
        return {}

# NOTE: Monoprice's Xantech-style interface also supports saving the current volume 
# as a max volume limiter: (!{z#}MX+).  We are not adding support for this, especially
# since it might be easier to implement in software here for use cases where no Keypads
# or other controllers exist that connect to the amplifier.

####

@ns.route('/<int:id>/power')
class ZonePowerToggle(Resource):
    def post(self, zone_id):
        raSerial.writeCommand("!" + zone_id + "PT+")
        return {}

@ns.route('/<int:id>/power/on')
class ZonePowerOn(Resource):
    def post(self, zone_id):
        raSerial.writeCommand("!" + zone_id + "PR1+")
        return {}

@ns.route('/<int:id>/power/off')
class ZonePowerOn(Resource):
    def post(self, zone_id):
        raSerial.writeCommand("!" + zone_id + "PR0+")
        return {}

####

@ns.route('/<int:id>/mute')
class ZoneMuteToggle(Resource):
    def post(self, zone_id):
        raSerial.writeCommand("!" + zone_id + "MT+")
        return {}

@ns.route('/<int:id>/mute/on')
class ZoneMuteOn(Resource):
    def post(self, zone_id):
        raSerial.writeCommand("!" + zone_id + "MU1+")
        return {}

@ns.route('/<int:id>/mute/off')
class ZoneMuteOn(Resource):
    def post(self, zone_id):
        raSerial.writeCommand("!" + zone_id + "MU0+")
        return {}

####

# NOTE: The Monoprice implementation only has two "sources": LINE and BUS and uses
# a different Channel Select (CS) selection, instead of Source Select (SS), plus
# a toggle since there are only two channels.  To support, this COULD be configurable
# to either have a Channel Select or Source Select APIs added.

@ns.route('/<int:id>/source/<int:source_id>')
class ZoneSourceSelect(Resource):
    def post(self, zone_id, source_id):
        raSerial.writeCommand("!" + zone_id + "SS" + source_id + "+")
        return {}

####

@ns.route('/<int:id>/balance/left')
class ZoneBalanceLeft(Resource):
    def post(self, zone_id):
        raSerial.writeCommand("!" + zone_id + "BL+")
        return {}

@ns.route('/<int:id>/balance/right')
class ZoneBalanceLeft(Resource):
    def post(self, zone_id):
        raSerial.writeCommand("!" + zone_id + "BR+")
        return {}


@ns.route('/<int:id>/bass/up')
class ZoneBassUp(Resource):
    def post(self, zone_id):
        raSerial.writeCommand("!" + zone_id + "BI+")
        return {}

@ns.route('/<int:id>/bass/down')
class ZoneBassDown(Resource):
    def post(self, zone_id):
        raSerial.writeCommand("!" + zone_id + "BD+")
        return {}


@ns.route('/<int:id>/treble/up')
class ZoneTrebleUp(Resource):
    def post(self, zone_id):
        raSerial.writeCommand("!" + zone_id + "TI+")
        return {}

@ns.route('/<int:id>/treble/down')
class ZoneTrebleDown(Resource):
    def post(self, zone_id):
        raSerial.writeCommand("!" + zone_id + "TD+")
        return {}