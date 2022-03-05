import traci

from src.trafficLight.TrafficLight import TrafficLight
from src.vehicleControl import isVehicleKnown
from src.vehicles.Stop import Stop


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
        return TrafficLight(traci.vehicle.getNextTLS(self.__id)[0])

    def getNthTrafficLightAhead(self, n=1):
        n -= 1
        return TrafficLight(traci.vehicle.getNextTLS(self.__id)[n])

    def isOnTrack(self):
        return isVehicleKnown(self.getId())

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

    def getFollower(self):
        return AbstractVehicle(traci.vehicle.getFollower(self.__id))

    def getNthFollower(self, n=1):
        current = self.getFollower()
        n -= 1
        while n > 0:
            current = current.getFollower(current)
        return current

    def getLeader(self):
        return AbstractVehicle(traci.vehicle.getLeader(self.__id))

    def getNthLeader(self, n=1):
        current = self.getLeader()
        n -= 1
        while n > 0:
            current = current.getLeader(current)
        return current

    def isStopped(self):
        return self.getAcceleration() == 0 and self.getSpeed() == 0

    def isBreaking(self):
        return self.getAcceleration() < 0

    def isJammed(self):

        if not self.isStopped():
            return False

        follower = self.getFollower()
        leader = self.getLeader()

        if follower.isOnTrack() and leader.isOnStrack():
            return follower.isStopped() and leader.isStopped()

        if follower.isOnTrack():
            return follower.isStopped()

        if leader.isOnTrack():
            return leader.isStopped()

    def getNextStop(self):
        return Stop(traci.vehicle.getNextStops(self.getId())[0])

    def getNthNextStop(self, n=1):
        n -= 1
        return Stop(traci.vehicle.getNextStops(self.getId()[n]))

    def getCurrentLane(self):
        return traci.vehicle.getLaneID(self.getId())

    # Probably not needed

    # def getUpcomingRoute(self):
    #     upcomingRoute = []
    #
    #     if self.isOnTrack():
    #         try:
    #             routeEdges = self.getRoute()
    #             edgeId = self.getNextEdgeId()
    #             isAfter = False
    #
    #             for edge in routeEdges:
    #
    #                 if edgeId == edge or isAfter:
    #                     isAfter = True
    #                     upcomingRoute.append(edgeId)
    #         except Exception as e:
    #             pass
    #
    #     return upcomingRoute

    # Probably not needed

    # def getAllUpcomingTrafficLightsInOrder(self):
    #     upcomingRoute = self.getUpcomingRoute()
    #     upcomingTrafficLights = []
    #     for edge in upcomingRoute:
    #         net = Net()
    #         nodeId = net.getNodeIdOfEdge(edge)
    #
    #         if traci.trafficlight.getIDList().__contains__(nodeId):
    #             upcomingTrafficLights.append(nodeId)
    #
    #     return upcomingTrafficLights

    def getSpeed(self):
        return traci.vehicle.getSpeed(self.__id)

    def getAcceleration(self):
        return traci.vehicle.getAcceleration(self.__id)

    def getPassengerCount(self):
        # todo
        return 0
