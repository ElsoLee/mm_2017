#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : build_transformation_network.py
from matplotlib import pyplot
from entities.arc import Arc
from entities.node import Node
from entities.schedule import Schedule
from network_building.build_network import build_network
from network_building.utility import *


def initialize_network(schedule_list, recovery_start_time, recovery_end_time, station_time_band, turnaround_time):
    node_dictionary = {}
    station_list = []
    for schedule in schedule_list:
        if schedule.departure_airport not in station_list:
            station_list.append(schedule.departure_airport)
        if schedule.arrive_airport not in station_list:
            station_list.append(schedule.arrive_airport)
    start_time, _ = get_segment_time(
        time=recovery_start_time,
        station_time_band=station_time_band
    )
    _, end_time = get_segment_time(
        time=recovery_end_time,
        station_time_band=station_time_band
    )
    time = start_time + station_time_band - 1
    while time <= end_time:
        for station in station_list:
            node_key = get_node_key(
                station_name=station,
                segment_start_time=start_time,
                segment_end_time=time
            )
            node_dictionary[node_key] = Node(
                station_name=station,
                segment_start_time=start_time,
                segment_end_time=time
            )
        start_time = time + 1
        time = start_time + station_time_band - 1
    for schedule in schedule_list:
        source_station_name = schedule.departure_airport
        departure_time = schedule.departure_time
        segment_start_time, segment_end_time = get_segment_time(
            time=departure_time,
            station_time_band=station_time_band
        )
        source_node_key = get_node_key(
            station_name=source_station_name,
            segment_start_time=segment_start_time,
            segment_end_time=segment_end_time
        )
        if source_node_key not in node_dictionary:
            continue
        mark_time = node_dictionary[source_node_key].mark_time
        node_dictionary[source_node_key].mark_time = min(mark_time, departure_time)
        target_station_name = schedule.arrive_airport
        available_time = schedule.arrive_time + turnaround_time
        segment_start_time, segment_end_time = get_segment_time(
            time=available_time,
            station_time_band=station_time_band
        )
        target_node_key = get_node_key(
            station_name=target_station_name,
            segment_start_time=segment_start_time,
            segment_end_time=segment_end_time
        )
        if target_node_key not in node_dictionary:
            continue
        mark_time = node_dictionary[target_node_key].mark_time
        node_dictionary[target_node_key].mark_time = min(mark_time, available_time)
    return_node_dictionary = {}
    count = 1
    for node in node_dictionary:
        if node_dictionary[node].mark_time < 2 ** 31 - 1:
            node = node_dictionary[node]
            node.node_id = count
            count += 1
            return_node_dictionary[node] = node
    return return_node_dictionary, count


def build_transformation_network(
        previous_count,
        schedule_list,
        sink_node_information_dictionary,
        marked_node_dictionary,
        turnaround_time,
        cost_function,
        station_time_band):
    def node_cmp(source_node, target_node):
        if source_node.mark_time > target_node.mark_time:
            return 1
        if source_node.mark_time < target_node.mark_time:
            return -1
        return 0

    count = previous_count
    node_dictionary = marked_node_dictionary
    node_list = [marked_node_dictionary[node_key] for node_key in marked_node_dictionary]
    sorted(node_list, cmp=node_cmp)
    arc_list = []
    cost_dictionary = {}
    while node_list:
        sorted(node_list, cmp=node_cmp)
        source_node = node_list[0]
        del node_list[0]
        source_mark_time = source_node.mark_time
        source_station_name = source_node.station_name
        for schedule in schedule_list:
            if schedule.departure_airport == source_station_name:
                plane_id = schedule.plane_no
                flight_id = schedule.flight_no
                target_station = schedule.arrive_airport
                duration = schedule.duration
                departure_time = max(source_mark_time, schedule.departure_time)
                available_time = departure_time + duration + turnaround_time
                sink_node_border = sink_node_information_dictionary[(plane_id, target_station)]
                if available_time > sink_node_border:
                    continue
                segment_start_time, segment_end_time = get_segment_time(
                    time=available_time,
                    station_time_band=station_time_band
                )
                target_node_key = get_node_key(target_station, segment_start_time, segment_end_time)
                if target_node_key not in node_dictionary:
                    new_target_node = Node(
                        node_id=count,
                        mark_time=available_time,
                        segment_start_time=segment_start_time,
                        segment_end_time=segment_end_time,
                        station_name=target_station,
                    )
                    new_target_node.plane_id_list.append(plane_id)
                    count += 1
                    node_dictionary[target_node_key] = new_target_node
                    node_list.append(new_target_node)
                else:
                    mark_time = min(
                        node_dictionary[target_node_key].mark_time,
                        available_time
                    )
                    node_dictionary[target_node_key].mark_time = mark_time
                    node_dictionary[target_node_key].plane_id_list.append(plane_id)
                    for i in range(len(node_list)):
                        if node_list[i].node_id == node_dictionary[target_node_key].node_id:
                            node_list[i].mark_time = mark_time
                            node_list[i].plane_id_list.append(plane_id)
                source_node.plane_id_list.append(plane_id)
                arc_list.append(Arc(source_node, node_dictionary[target_node_key], flight_id))
                cost_dictionary[(
                    source_node.node_id,
                    node_dictionary[target_node_key].node_id,
                    flight_id
                )] = cost_function(max(0, departure_time + duration - schedule.arrive_time))
    return node_dictionary, arc_list, cost_dictionary


if __name__ == '__main__':
    schedule_list = []
    schedule_list.append(
        Schedule([
            11,
            string_to_timestamp('2017-9-17 14:10'),
            string_to_timestamp('2017-9-17 15:20'),
            'BOI',
            'SEA',
            0,
            1,
        ])
    )
    schedule_list.append(
        Schedule([
            12,
            string_to_timestamp('2017-9-17 16:05'),
            string_to_timestamp('2017-9-17 17:00'),
            'SEA',
            'GEG',
            0,
            1,
        ])
    )
    schedule_list.append(
        Schedule([
            13,
            string_to_timestamp('2017-9-17 17:40'),
            string_to_timestamp('2017-9-17 18:40'),
            'GEG',
            'SEA',
            0,
            1,
        ])
    )
    schedule_list.append(
        Schedule([
            14,
            string_to_timestamp('2017-9-17 19:20'),
            string_to_timestamp('2017-9-17 20:35'),
            'SEA',
            'BOI',
            0,
            1,
        ])
    )
    schedule_list.append(
        Schedule([
            21,
            string_to_timestamp('2017-9-17 15:45'),
            string_to_timestamp('2017-9-17 17:00'),
            'SEA',
            'BOI',
            0,
            2,
        ])
    )
    schedule_list.append(
        Schedule([
            22,
            string_to_timestamp('2017-9-17 17:40'),
            string_to_timestamp('2017-9-17 18:50'),
            'BOI',
            'SEA',
            0,
            2,
        ])
    )
    schedule_list.append(
        Schedule([
            23,
            string_to_timestamp('2017-9-17 19:30'),
            string_to_timestamp('2017-9-17 20:30'),
            'SEA',
            'GEG',
            0,
            2,
        ])
    )
    schedule_list.append(
        Schedule([
            24,
            string_to_timestamp('2017-9-17 21:15'),
            string_to_timestamp('2017-9-17 22:15'),
            'GEG',
            'SEA',
            0,
            2,
        ])
    )
    schedule_list.append(
        Schedule([
            31,
            string_to_timestamp('2017-9-17 15:15'),
            string_to_timestamp('2017-9-17 16:20'),
            'GEG',
            'PDX',
            0,
            3,
        ])
    )
    schedule_list.append(
        Schedule([
            32,
            string_to_timestamp('2017-9-17 17:30'),
            string_to_timestamp('2017-9-17 18:30'),
            'PDX',
            'GEG',
            0,
            3,
        ])
    )
    schedule_list.append(
        Schedule([
            33,
            string_to_timestamp('2017-9-17 19:10'),
            string_to_timestamp('2017-9-17 20:20'),
            'GEG',
            'PDX',
            0,
            3,
        ])
    )
    schedule_list.append(
        Schedule([
            34,
            string_to_timestamp('2017-9-17 21:00'),
            string_to_timestamp('2017-9-17 21:55'),
            'PDX',
            'GEG',
            0,
            3,
        ])
    )
    turnaround_time = 40 * 60
    station_time_band = 30 * 60
    # network_node_dictionary, network_arc_list = build_network(
    #     schedule_list,
    #     string_to_timestamp('9-17 13:30'),
    #     string_to_timestamp('9-17 23:59'),
    #     station_time_band,
    #     turnaround_time
    # )
    # for arc in network_arc_list:
    #     arc.print_information()
    # draw_figure(network_arc_list, 30, ['BOI', 'SEA', 'GEG', 'PDX'])


    marked_node_dictionary, count = initialize_network(
        schedule_list=schedule_list,
        recovery_start_time=string_to_timestamp('2017-9-17 13:10'),
        recovery_end_time=string_to_timestamp('2017-9-17 23:59'),
        station_time_band=station_time_band,
        turnaround_time=turnaround_time
    )
    node_dictionary, arc_list, cost_dictionary = build_transformation_network(
        previous_count=count,
        schedule_list=schedule_list,
        sink_node_information_dictionary={
            (1, 'BOI'): string_to_timestamp('2017-9-17 23:59'),
            (1, 'SEA'): string_to_timestamp('2017-9-17 23:59'),
            (1, 'GEG'): string_to_timestamp('2017-9-17 23:59'),
            (1, 'PDX'): string_to_timestamp('2017-9-17 23:59'),
            (2, 'BOI'): string_to_timestamp('2017-9-17 23:59'),
            (2, 'SEA'): string_to_timestamp('2017-9-17 23:59'),
            (2, 'GEG'): string_to_timestamp('2017-9-17 23:59'),
            (2, 'PDX'): string_to_timestamp('2017-9-17 23:59'),
            (3, 'BOI'): string_to_timestamp('2017-9-17 23:59'),
            (3, 'SEA'): string_to_timestamp('2017-9-17 23:59'),
            (3, 'GEG'): string_to_timestamp('2017-9-17 23:59'),
            (3, 'PDX'): string_to_timestamp('2017-9-17 23:59'),
        },
        marked_node_dictionary=marked_node_dictionary,
        turnaround_time=turnaround_time,
        cost_function=lambda x: x,
        station_time_band=station_time_band
    )
    draw_figure(arc_list, 30, ['BOI', 'SEA', 'GEG', 'PDX'])
