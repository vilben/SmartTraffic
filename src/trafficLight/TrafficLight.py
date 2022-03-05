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
        self.__skipPhasesUntil('Rr')

    def setToGreen(self):
        self.__skipPhasesUntil('Gg')

    def setToYellowOrGreen(self):
        self.__skipPhasesUntil('GgYy')

    def advanceToAnyYellow(self):
        if "y" not in traci.trafficlight.getRedYellowGreenState(self.getId()).lower():
            traci.trafficlight.setPhaseDuration(self.getId(), 0)

    def ensureAccess(self):
        if self.getCurrentPhase().lower() != "g":
            self.advanceToAnyYellow()

    def getCurrentPhase(self):
        return self.__currentPhase

    def getDistanceFromVehicle(self):
        return self.__distanceFromBus

    def setPhaseDuration(self, duration=10):
        traci.trafficlight.setPhaseDuration(self.getId(), duration)

    def __skipPhasesUntil(self, colors="GgYy"):
        # skip phases until phase is either 'G', 'R' or 'Y'

        if not colors.__contains__(self.getCurrentPhase()):
            self.setPhaseDuration(0)
