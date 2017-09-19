def get_flight_list(schedule_list):
    flight_set = set()

    for flight in schedule_list:
        flight_set.add(flight.flight_no)

    return list(flight_set)


def get_flight_count(arc_list):
    flight_set = set()
    for arc in arc_list:
        flight_set.add(arc.flight_id)

    return list(flight_set)

