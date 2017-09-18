def get_flight_list(schedule_list):
    flight_set = set()

    for flight in schedule_list:
        flight_set.add(flight.flight_no)

    return list(flight_set)

