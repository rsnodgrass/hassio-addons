# NOTE: Everywhere Monoprice is referenced, this also applies to the Dayton Audio DAX66
#
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

# /api/xantech8/zones
ns = api.namespace('xantech8', description='Zone operations')

@ns.route('/')
class EquipmentList(Resource):
    def get(self):
       """
        Return a list of all instances of Xantech8 controllers configured for this server
        """
        details = {
            "controllers": {
                "xantech8": {
                    "name": "Xantech 8-Zone Audio (Second Floor)",
                    "url": "/xantech8/<slug>" },
                "xantech8-2": {
                    "name": "Xantech 8-Zone Audio (Basement)",
                    "url": "/xantech8/<slug2>"
                }
            }
        }
        return json.dumps(details)


@ns.route('/<int:hardware_id>')
class ZoneCollection(Resource):

    @api.param('hardware_id', 'Identifier for which physical hardware to control')
    @api.marshal_list_with(zone)
    def get(self):

        # FIXME: move all the following into initial setup

        max_zones = 8
        zone_map = _init_name_mapping('Zone', max_zones)

        # NOTE: Monoprice only supports two inputs (bus/line), not source mapping!
        max_sources = 8
        source_map = _init_name_mapping('Source', max_sources)
        source_map[1] = 'Sonos' # override
        source_map[2] = 'Home Theater' # override

        zone_config = {
            'type': 'xantech', # types: [ "xantech", "monoprice", "daytona-audio" ]

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

@ns.route('/<string:hardwareid>/<int:zone_id>')
@api.param('hardware_id', 'Identifier for which physical hardware to control')
@api.param('zone_id', 'Identifier for the zone')
@api.response(404, 'Zone not found')
class ZoneStatus(Resource):

    #@api.marshal_with(zone)
    def get(self, zone_id):
        """Return the current status details for this zone"""
        state = xantechInterface.get_zone_state(zone_id)
        if state == None:
            # FIXME: return error
            return False

        # FIXME: inject additional info into zone?

        return state

    # FIXME: allow renaming a zone, or setting other properties directly
    def put(self, zone_id):
        """Update details for this zone"""
        # { "name": "Master Bedroom", "volume": 10, "power": off, "mute": off, "source": 1 }
        # bass, treble, balance, channel
        # public-address / do-not-disturb
        return {}

####

]# we could have gone all the way to 11, but instead decided on the range 0-100%
@ns.route('/<int:zone_id>/volume/<int:percentage>')
@api.param('zone_id', 'Identifier for the zone')
@api.param('level', 'Volume level 0–100')
@api.response(404, 'Zone not found')
class ZoneVolumeLevel(Resource):
    def post(self, zone_id, percentage):
        """Explicitly set the zone's volume level"""

        if percentage < 0 or percentage > 100:
            log.error("Received invalid value %d for zone %d volume level, must be 0-100", zone_id percentage)
            return

        # While actual attenuation steps for Xantech is 0-38 (non-linearly from -78.75 db to 0 db),
        # for simplicity of API, we use range from 0-100% even though increase by 1%  <may not
        # necessarily change volume if it remains within the same dB attenuation step.
        attenuation_level = (38 * percentage) / 100
        xantechInterface.write_command("!" + zone_id + "VO" + attenuation_level + "+")
        return {}

@ns.route('/<int:zone_id>/volume/up')
class ZoneVolumeUp(Resource):
    def post(self, zone_id):
        """Increase the zone's volume level"""
        xantechInterface.write_command("!" + zone_id + "VI+")
        return {}

@ns.route('/<int:zone_id>/volume/down')
class ZoneVolumeDown(Resource):
    def post(self, zone_id):
        """Decrease the zone's volume level"""
        xantechInterface.write_command("!" + zone_id + "VD+")
        return {}

# NOTE: Monoprice's Xantech-style interface also supports saving the current volume 
# as a max volume limiter: (!{z#}MX+).  We are not adding support for this, especially
# since it might be easier to implement in software here for use cases where no Keypads
# or other controllers exist that connect to the amplifier.

####

@ns.route('/<int:zone_id>/power/on')
class ZonePowerOn(Resource):
    def post(self, zone_id):
        """Power this zone on"""
        xantechInterface.write_command("!" + zone_id + "PR1+")
        return {}

@ns.route('/<int:zone_id>/power/off')
class ZonePowerOff(Resource):
    def post(self, zone_id):
        """Power this zone off"""
        xantechInterface.write_command("!" + zone_id + "PR0+")
        return {}

####

@ns.route('/<int:zone_id>/mute/on')
class ZoneMuteOn(Resource):
    def post(self, zone_id):
        """Mute this zone"""
        xantechInterface.write_command("!" + zone_id + "MU1+")
        return {}

@ns.route('/<int:zone_id>/mute/off') 
class ZoneMuteOff(Resource):
    def post(self, zone_id):
        """Unmute this zone"""
        xantechInterface.write_command("!" + zone_id + "MU0+")
        return {}

####

# NOTE: The Monoprice implementation only has two "sources": LINE and BUS and uses
# a different Channel Select (CS) selection, instead of Source Select (SS), plus
# a toggle since there are only two channels.  To support, this COULD be configurable
# to either have a Channel Select or Source Select APIs added.

@ns.route('/<int:zone_id>/source/<int:source_id>')
class ZoneSourceSelect(Resource):
    def post(self, zone_id, source_id):
        """Select which source the zone should play"""
        xantechInterface.write_command("!" + zone_id + "SS" + source_id + "+")
        return {}

####

# FIXME: Normalize balance to allow sliders

@ns.route('/<int:zone_id>/balance/left')
class ZoneBalanceLeft(Resource):
    def post(self, zone_id):
        """Dial this zone's balance to the left"""
        xantechInterface.write_command("!" + zone_id + "BL+")
        return {}

@ns.route('/<int:zone_id>/balance/right')
class ZoneBalanceRight(Resource):
    def post(self, zone_id):
        """Dial this zone's balance to the right"""
        xantechInterface.write_command("!" + zone_id + "BR+")
        return {}

# FIXME: Normalize treble adjustments 0-100%...default is 50%?  E.g. 7 is 0 dB on Xantech, vs 14 is +14 dB

@ns.route('/<int:zone_id>/bass/up')
class ZoneBassUp(Resource):
    def post(self, zone_id):
        """Increase the base for this zone"""
        xantechInterface.write_command("!" + zone_id + "BI+")
        return {}

@ns.route('/<int:zone_id>/bass/down')
class ZoneBassDown(Resource):
    def post(self, zone_id):
        """Decrease the base for this zone"""
        xantechInterface.write_command("!" + zone_id + "BD+")
        return {}

# FIXME: Normalize treble adjustments 0-100%...default is 50%?  E.g. 7 is 0 dB on Xantech, vs 14 is +14 dB

@ns.route('/<int:zone_id>/treble/up')
class ZoneTrebleUp(Resource):
    def post(self, zone_id):
        """Increase the treble for this zone"""
        xantechInterface.write_command("!" + zone_id + "TI+")
        return {}

@ns.route('/<int:zone_id>/treble/down')
class ZoneTrebleDown(Resource):
    def post(self, zone_id):
        """Decrease the treble for this zone"""
        xantechInterface.write_command("!" + zone_id + "TD+")
        return {}
