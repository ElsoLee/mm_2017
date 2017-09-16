from entities.schedules import Schedules


def schedule_preprocessing():
    with open('./data/Schedules.csv', 'r') as f:
        lines = f.readlines()

        flights = []
        for l in lines:
            items = l.split(',')
            flights.append(Schedules(items))

        return flights

