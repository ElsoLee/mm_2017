
class Aircraft(object):
    def __init__(self, split_str):
        self.plane_no = split_str[0]
        self.plane_type = split_str[1]
        self.first_available_time = int(split_str[2])
        self.last_available_time = int(split_str[3])
        self.init_airport = split_str[4]
        self.seats = split_str[5]

