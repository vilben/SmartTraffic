import traci


class TrafficLight:

    def __init__(self, id):
        self.__id = id

    def setToRed(self):
        traci.trafficlight.setRedYellowGreenState(self.__id, )
