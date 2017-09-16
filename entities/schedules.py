
class Schedules(object):
    def __init__(self, split_line):
        self.flight_no = split_line[0]
        self.departure_time = int(split_line[1])
        self.arrive_time = int(split_line[2])
        self.departure_airport = split_line[3]
        self.arrive_airport = split_line[4]
        self.plane_type = split_line[5]
        self.plane_no = split_line[6]
        self.available_time = self.departure_time
        self.duration = self.arrive_time - self.departure_time

    def __lt__(self, other):
        return self.available_time < other.available_time
