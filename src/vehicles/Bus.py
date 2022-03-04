import traci


class Bus:

    def __init__(self, id):
        self.__id = id

    def getId(self):
        return self.__id

    def getCurrentPosition(self):
        return traci.vehicle.getPosition(self.__id)

    def getEmissions(self):
        return traci.vehicle.getCO2Emission(self.__id)

    def getNextTrafficLight(self):
        return traci.vehicle.getNextTLS(self.__id)

    def getUpcomingRoute(self):
        routeEdges = traci.vehicle.getRoute(self.__id)
        currentPosition = self.getCurrentPosition()

        index = 0
        isAfter = False

        upcomingRoute = []

        for edge in routeEdges:
            if edge == currentPosition or isAfter:
                isAfter = True
                upcomingRoute[index] = edge
                index += 1

        return upcomingRoute

    def getAllUpcomingTrafficLightsInOrder(self):
        upcomingRoute = self.getUpcomingRoute()

        upcomingTrafficLights = []
        index = 0

        for edge in upcomingRoute:
            if traci.trafficlight.getIDList().__contains__(edge):
                upcomingTrafficLights[index] = edge
                index += 1

        return upcomingTrafficLights

    def getSpeed(self):
        return traci.vehicle.getSpeed(self.__id)

    def getPassengerCount(self):
        # todo
        return 0