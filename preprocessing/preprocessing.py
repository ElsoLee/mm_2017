from entities.schedule import Schedule
from entities.aircraft import Aircraft

def aircraft_preprocessing():
    with open('../data/Aircrafts.csv', 'r') as f:
        lines = f.readlines()

        aircrafts = []
        for l in lines:
            items = l.split(',')
            aircrafts.append(Aircraft(items))

        return aircrafts


def schedule_preprocessing():
    with open('../data/Schedules.csv', 'r') as f:
        lines = f.readlines()

        flights = []
        for l in lines:
            items = l.split(',')
            flights.append(Schedule(items))

        return flights


def generate_sink_node():
    flights = schedule_preprocessing()
    aircrafts = aircraft_preprocessing()

    _type_9_aircrafts = [air for air in aircrafts if air.plane_type == '9']
    _type_9_flights = [f for f in flights if f.plane_type == '9']

    station_sink = {}

    for air in _type_9_aircrafts:
        fls = [f for f in _type_9_flights if f.plane_no == air.plane_no]
        fls.sort()
        last_flight = fls[len(fls) - 1]

        station_sink[
            (last_flight.plane_no, last_flight.arrive_airport)] = air.last_available_time + last_flight.duration

    return station_sink
