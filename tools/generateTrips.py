from distutils.command.config import config
import yaml
import random

class TripGenerator:

    config_yaml = ""
    trip_types = []

    def __init__(self, config_yaml):
        self.config_yaml = config_yaml

    def print(self):
        print(self.config_yaml)


    def parse(self):
        self.depart_min = self.config_yaml['depart_min']
        self.depart_max = self.config_yaml['depart_max']
        self.edges = self.config_yaml['edges']
        self.generate_random = self.config_yaml['generate_random']

        self.__parseTripTypes()


    def buildTrips(self):

        if len(self.trip_types) == 0 :
            self.parse(self)

        total_trips = 0

        if(self.generate_random > 0):
            total_trips += self.generate_random

        for trip in self.trip_types:
            total_trips += trip.count

        available_slots = list(range(0, total_trips + 1))
        generated_trips = []

        for random_trip in range(0, self.generate_random):

            start_pos = random.randint(1, self.edges)
            end_pos = random.randint(1, self.edges)

            slot_pos = random.randint(1, len(available_slots) - 1)
            slot = available_slots[slot_pos]
            del available_slots[slot_pos]

            generated_trips.append(Trip(start_pos, end_pos, slot, slot))

        for trip_type in self.trip_types:

            for trip in range(0, trip_type.count):

                slot_pos = random.randint(1, len(available_slots) - 1)
                slot = available_slots[slot_pos]
                del available_slots[slot_pos]

                generated_trips.append(Trip(trip_type.from_edge, trip_type.to_edge, slot, slot))

        generated_trips.sort(key=lambda t: t.id, reverse=False)

        for trin in generated_trips:
            trin.print()


    def __parseTripTypes(self):

        for trip in self.config_yaml['trips']:
            self.trip_types.append(TripType(trip))

class Trip:
    def __init__(self, from_edge, to_edge, depart, id):
        self.from_edge = from_edge
        self.to_edge = to_edge
        self.depart = depart
        self.id = id

    def getId(self):
        return self.id

    def print(self):
        print('<trip id="{0}" depart="{1}" from="e{2}" to="e{3}"/>'.format(self.id, self.depart, self.from_edge, self.to_edge))


class TripType:

    def __init__(self, config):
        self.from_edge = config['from']
        self.to_edge = config['to']
        self.count = config['count']


if __name__ == "__main__":

    config_file  = "exampleTrips.yaml"

    with open(config_file, 'r') as file:
        docs = yaml.safe_load(file)

        generator = TripGenerator(docs)
        generator.parse()
        generator.buildTrips()