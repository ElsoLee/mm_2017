#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : utility.py
import time
from datetime import datetime, timedelta
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, MinuteLocator
import matplotlib.pyplot as plt
from numpy import arange


def get_node_key(station_name, segment_start_time, segment_end_time):
    return station_name + ':' + timestamp_to_string(segment_start_time) + '-' + timestamp_to_string(segment_end_time)


def get_segment_time(time, station_time_band):
    quotation = time // station_time_band
    return station_time_band * quotation, station_time_band * (quotation + 1) - 1


def get_cost_dictionary_key(source_node_id, target_node_id, flight_id):
    return str(source_node_id) + '-' + str(target_node_id) + '-' + str(flight_id)


def timestamp_to_string(timestamp):
    return time.strftime('%m-%d %H:%M', time.localtime(timestamp))


def string_to_timestamp(time_string):
    return time.mktime(time.strptime(time_string, '%Y-%m-%d %H:%M'))


def draw_figure(arc_list, station_time_band, label_list=None):
    group_labels = []
    if label_list is None:
        for arc in arc_list:
            if arc.source_node.station_name not in group_labels:
                group_labels.append(arc.source_node.station_name)
            if arc.target_node.station_name not in group_labels:
                group_labels.append(arc.target_node.station_name)
    else:
        group_labels = label_list
    label_dictionary = {}
    for i in range(len(group_labels)):
        label_dictionary[group_labels[i]] = i

    fig, ax = plt.subplots()

    max_time = arc_list[0].source_node.mark_time
    min_time = arc_list[0].source_node.mark_time
    for arc in arc_list:
        y = [arc.source_node.station_name, arc.target_node.station_name]
        x = [arc.source_node.mark_time, arc.target_node.mark_time]
        max_time = max(max_time, arc.source_node.mark_time, arc.target_node.mark_time)
        min_time = min(max_time, arc.source_node.mark_time, arc.target_node.mark_time)
        y = map(lambda l: label_dictionary[l], y)
        x = map(lambda t: datetime.fromtimestamp(t), x)
        ax.plot(x, y, marker='o', c='blue')

    ax.set_xlim(datetime.fromtimestamp(min_time), datetime.fromtimestamp(max_time))

    ax.xaxis.set_major_locator(MinuteLocator(arange(0, 59, station_time_band)))
    ax.xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))

    plt.yticks([i for i in range(len(group_labels))], tuple(group_labels))

    fig.autofmt_xdate()
    fig.tight_layout()

    plt.show()
