#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : build_network.py
import time

from entities.arc import Arc
from entities.node import Node
from network_building.utility import *
from preprocessing.preprocessing import *


def build_network(schedule_list, recovery_start_time, recovery_end_time, station_time_band, turnaround_time):
    node_dictionary = {}
    arc_dictionary = {}
    schedule_list.sort()
    count = 1
    for schedule in schedule_list:
        if schedule.departure_time >= recovery_start_time and schedule.arrive_time <= recovery_end_time:
            segment_start_time, segment_end_time = get_segment_time(
                time=schedule.departure_time,
                station_time_band=station_time_band
            )
            source_node_key = get_node_key(
                station_name=schedule.departure_airport,
                segment_start_time=segment_start_time,
                segment_end_time=segment_end_time
            )
            if source_node_key not in node_dictionary:
                node_dictionary[source_node_key] = Node(
                    node_id=count,
                    mark_time=schedule.departure_time,
                    segment_start_time=segment_start_time,
                    segment_end_time=segment_end_time,
                    station_name=schedule.departure_airport
                )
                count += 1
            else:
                mark_time = min(node_dictionary[source_node_key].mark_time, schedule.departure_time)
                node_dictionary[source_node_key].mark_time = mark_time
            available_time = schedule.arrive_time + turnaround_time
            segment_start_time, segment_end_time = get_segment_time(
                time=available_time,
                station_time_band=station_time_band
            )
            target_node_key = get_node_key(
                station_name=schedule.arrive_airport,
                segment_start_time=segment_start_time,
                segment_end_time=segment_end_time
            )
            if target_node_key not in node_dictionary:
                node_dictionary[target_node_key] = Node(
                    node_id=count,
                    mark_time=available_time,
                    segment_start_time=segment_start_time,
                    segment_end_time=segment_end_time,
                    station_name=schedule.arrive_airport
                )
                count += 1
            else:
                available_time = schedule.departure_time + schedule.duration + turnaround_time
                mark_time = min(node_dictionary[target_node_key].mark_time, available_time)
                node_dictionary[target_node_key].mark_time = mark_time
            flight_id = schedule.flight_no
            if flight_id not in arc_dictionary:
                arc_dictionary[flight_id] = Arc(
                    source_node=node_dictionary[source_node_key],
                    target_node=node_dictionary[target_node_key],
                    flight_id=flight_id
                )
    arc_list = []
    for arc in arc_dictionary:
        arc_list.append(arc_dictionary[arc])
    return node_dictionary, arc_list
