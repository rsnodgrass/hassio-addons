# Not implemented:
#
# - explicitly setting bass/treble/balance: while easy to add, but unclear if
#   useful except during initial amp setup for advanced use cases, plus the 
#   explicit lookup table values complex to document (and may vary by device)
# - current sense (audio) and video sense queries ... 12V?
# - video switching (for capable matrix controller models)

import os   
import json
import logging

from flask import request
from flask_restplus import Resource
#from bridge.api.manager.serializers import zone
from bridge.api.restplus import api

log = logging.getLogger(__name__)

# /api/xantech/zones
ns = api.namespace('zones', description='Audio zone operations')

raSerial = None # FIXME: init raSerial XantechSerial

@ns.route('/')
class ZoneCollection(Resource):
    
    def _init_name_mapping(count, name_prefix):
        map = {}
        for i in range(count):
            map[i] = name_prefix + ' ' + i
        return map

    @api.marshal_list_with(zone)
    def get(self):

        # FIXME: move all the following into initial setup

        # NOTE: for Xantech, only first 6 zones support amplification, the last 2 are pre-amps

        max_zones = 8
        zone_map = _init_name_mapping('Zone', max_zones)

        # NOTE: Monoprice only supports two inputs (bus/line), not source mapping!
        max_sources = 8
        source_map = _init_name_mapping('Source', max_sources)
        source_map[1] = 'Sonos' # override
        source_map[2] = 'Home Theater' # override

        zone_config = {
            'module': 'xantech_mza',

            'max_zones': max_zones, # configurable
            'zones': { # FIXME: configurable name override
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
            'sources': source_map, # FIXME: configurable name override
        } 

        # FIXME: should this return the current state for all zones?? Could lead to trouble...

        return zone_config

@ns.route('/<int:id>')
@api.response(404, 'Zone not found')
class ZoneStatus(Resource):

    def _convert_state_to_map(serialized_state):
        state = {}
        for data in serialized_state.split():
            # verify the serial response matches the zone_id we just wrote data for
            if data[0] == '#':
                state['zone'] = int(data[1:][0:1])

            # for each type of data in the response, map into the state structure
            # (not all may be returned, depending on what features the amplifier supports)
            data_type = data[0:1]
            if data_type in ['PR', 'PO']: # Xantech / Monoprice
                state['power'] = (data[2] == '1') # bool
                
            elif 'SS' == data_type: # Xantech
                state['source'] = int(data[2:])

            elif 'VO' == data_type:
                # map the 38 physical attenuation levels into 0-100%
                attenuation_level = int(data[2:])
                state['volume'] = round((100 * attenuation_level) / 38)

            elif 'MU' == data_type:
                state['mute'] = (data[2] == '1') # bool

            elif 'TR' == data_type:
                state['treble'] = int(data[2:])

            elif 'BS' == data_type:
                state['bass'] = int(data[2:])

            elif 'BA' == data_type:
                state['balance'] = int(data[2:])

            elif 'LS' == data_type:
                # Xantech: linked; Monoprice: keypad status?
                state['linked'] = (data[2] == '1') # bool

            elif 'PS' == data_type: # Xantech
                state['paged'] = (data[2] == '1') # bool

            elif 'DT' == data_type: # Monoprice
                # ignore unknown datatype found on Monoprice amp
                state['dt_unknown'] = int(data[2:])

            elif 'PA' == data_type: # Monoprice
                state['pa'] = true # zone 1 to all outputs

            elif 'CH' == data_type: # Monoprice (channel)
                if data[2] == '1':
                    state['channel'] = 'line'
                else:
                    state['channel'] = 'bus'

            elif 'IS' == data_type: # Monoprice (audio input), seen in docs
                if data[2] == '1':
                    state['input'] = 'line'
                else:
                    state['input'] = 'bus'

            else:
                log.warning("Ignoring unknown zone %d state attribute '%s' found in: %s",
                            state['zone'], data_type, serialized_state)

        return state

    #@api.marshal_with(zone)
    def get(self, zone_id):
        # FIXME: if zone < 0 or zone > 8, error state
        raSerial.writeCommand("?" + zone_id + "ZD+")

        # example Xantech response:
        #   #{z#}ZS PR{0/1} SS{s#} VO{v#} MU{0/1} TR{bt#} BS{bt#} BA{b#} LS{0/1} PS{0/1}+
        # example Monoprice response:
        #   #{z#}ZS VO{v#} PO{0/1} MU{0/1} IS{0/1}+
        response = raSerial.readData()

        state = _convert_state_to_map(response)
        if state["zone"] != zone_id:
            log.error("Unknown state! Request for zone %s returned state for zone %d: %s",
                      zone_id, zone_id, response)
            return None # FIXME: return error!

        return state

####

]# we could have gone all the way to 11, but instead decided on the range 0-100%
@ns.route('/<int:id>/volume/<int:percentage>')
class ZoneVolumeLevel(Resource):
    def post(self, zone_id, percentage):

        # While actual attenuation steps for Xantech is 0-38 (non-linearly from -78.75 db to 0 db),
        # for simplicity of API, we use range from 0-100% even though increase by 1%  <may not
        # necessarily change volume if it remains within the same dB attenuation step.
        attenuation_level = (38 * percentage) / 100
        raSerial.writeCommand("!" + zone_id + "VO" + attenuation_level + "+")
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

@ns.route('/<int:id>/power/on')
class ZonePowerOn(Resource):
    def post(self, zone_id):
        raSerial.writeCommand("!" + zone_id + "PR1+")
        return {}

@ns.route('/<int:id>/power/off')
class ZonePowerOff(Resource):
    def post(self, zone_id):
        raSerial.writeCommand("!" + zone_id + "PR0+")
        return {}

####

@ns.route('/<int:id>/mute/on')
class ZoneMuteOn(Resource):
    def post(self, zone_id):
        raSerial.writeCommand("!" + zone_id + "MU1+")
        return {}

@ns.route('/<int:id>/mute/off') 
class ZoneMuteOff(Resource):
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
class ZoneBalanceRight(Resource):
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
