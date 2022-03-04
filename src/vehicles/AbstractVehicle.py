import traci

from src.net.Net import Net


class AbstractVehicle:

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

    def isOnTrack(self):
        if self.getRoute() != (0,):
            return True
        else:
            return False

    def getRoute(self):
        try:
            return traci.vehicle.getRoute(self.__id)
        except:
            return 0,

    def getNextEdgeId(self):
        if self.isOnTrack():
            laneId = traci.vehicle.getLaneID(self.__id)
            edgeId = traci.lane.getEdgeID(laneId)
            return edgeId
        return 0

    def getUpcomingRoute(self):
        upcomingRoute = []

        if self.isOnTrack():
            try:
                routeEdges = self.getRoute()
                edgeId = self.getNextEdgeId()
                isAfter = False

                for edge in routeEdges:

                    if edgeId == edge or isAfter:
                        isAfter = True
                        upcomingRoute.append(edgeId)
            except Exception as e:
                pass

        return upcomingRoute

    def getAllUpcomingTrafficLightsInOrder(self):
        upcomingRoute = self.getUpcomingRoute()
        upcomingTrafficLights = []
        for edge in upcomingRoute:
            net = Net()
            nodeId = net.getNodeIdOfEdge(edge)

            if traci.trafficlight.getIDList().__contains__(nodeId):
                upcomingTrafficLights.append(nodeId)

        return upcomingTrafficLights

    def getSpeed(self):
        return traci.vehicle.getSpeed(self.__id)

    def getPassengerCount(self):
        # todo
        return 0
