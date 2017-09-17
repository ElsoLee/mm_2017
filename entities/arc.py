#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : arc.py
from network_building.utility import *


class Arc(object):
    def __init__(self, source_node, target_node, flight_id):
        self.source_node = source_node
        self.target_node = target_node
        self.flight_id = flight_id

    def print_information(self):
        print get_node_key(
            self.source_node.station_name,
            self.source_node.segment_start_time,
            self.source_node.segment_end_time
        ) + '(' + timestamp_to_string(self.source_node.mark_time) + ') -> ' + get_node_key(
            self.target_node.station_name,
            self.target_node.segment_start_time,
            self.target_node.segment_end_time
        ) + '(' + timestamp_to_string(self.target_node.mark_time) + ')'
