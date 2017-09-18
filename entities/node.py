#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : node.py
import time

from network_building.utility import *


class Node(object):
    def __init__(self, station_name, node_id=0, mark_time=2 ** 31 - 1, segment_start_time=0, segment_end_time=0):
        self.node_id = node_id
        self.mark_time = mark_time
        self.segment_start_time = segment_start_time
        self.segment_end_time = segment_end_time
        self.station_name = station_name
        self.plane_id_list = []

    def __lt__(self, other):
        return self.segment_start_time < other.segment_start_time

    def print_information(self):
        print ('node_id', self.node_id)
        print ('mark_time', timestamp_to_string(self.mark_time))
        print ('segment_start_time', timestamp_to_string(self.segment_start_time))
        print ('segment_end_time', timestamp_to_string(self.segment_end_time))
        print ('station_name', self.station_name)
