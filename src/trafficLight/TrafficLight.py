import traci


class TrafficLight:
    # Constructor for tls gotten by bus.getNextTrafficLight
    def __init__(self, tls):
        self.__id = tls[0]
        self.__index = tls[1]
        self.__distanceFromBus = tls[2]
        self.__currentPhase = tls[3]

    def getId(self):
        return self.__id

    def setToRed(self):
        self.__skipPhasesUntil('R')

    def setToGreen(self):
        self.__skipPhasesUntil('G')

    def getCurrentPhase(self):
        return self.__currentPhase

    def getDistanceFromBus(self):
        return self.__distanceFromBus

    def __skipPhasesUntil(self, color='G'):
        # skip phases until phase is either 'G', 'R' or 'Y'
        if self.getCurrentPhase() != color and self.getCurrentPhase() != color.lower():
            traci.trafficlight.setPhaseDuration(self.getId(), 0)
