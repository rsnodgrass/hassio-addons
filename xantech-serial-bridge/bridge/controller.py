import re
import logging

class MultiZoneController:
    def __init__(self, name, controller_module):
        self.name = name

        # FIXME: read yaml file

        self._max_zones = 8
        self._zone_map = _init_name_mapping(self._max_zones, "Zone")
        self._max_sources = 8
        self._source_map = _init_name_mapping(self._max_sources, "Source")

    def _init_name_mapping(count, name_prefix):
        map = {}
        for i in range(count):
            map[i] = name_prefix + ' ' + i
        return map

    # FIXME: one difference between Xantech and Monoprice is that the
    # prefix for change commands in Xantech is "!" and Monoprice it is ">"

    def is_valid_zone(zone_id):
        if zone_id <= 0:
            return False
        elif zone_id > self._max_zones:
            # FIXME: determine if valid based on configuration for amplifier (model, number of slaves, etc)
            return False
        return True

    def is_valid_source(source_id):
        if source_id <= 0:
            return False
        elif source_id > self._source_zones:
            # FIXME: determine if valid based on configuration for amplifier
            return False
        return True
