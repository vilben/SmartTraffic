class Stop:

    # [(lane, endPos, stoppingPlaceID, stopFlags, duration, until), ...]

    def __init__(self, stop):
        self.__lane = stop[0]
        self.__endPos = stop[1]
        self.__stoppingPlaceId = stop[2]
        self.__stopFlags = stop[3]
        self.__duration = stop[4]
        self.__until = stop[5]

    def isBusStop(self):
        # 1 * stopped + 2 * parking + 4 * personTriggered + 8 * containerTriggered +
        # 16 * isBusStop + 32 * isContainerStop + 64 * chargingStation +
        # 128 * parkingarea
        return self.__stopFlags >= 16

    def getLane(self):
        return self.__lane
