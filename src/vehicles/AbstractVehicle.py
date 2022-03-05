from lib2to3.pgen2.token import ISNONTERMINAL
import traci

from src.net.Net import Net
from src.vehicleControl import isVehicleKnown

class AbstractVehicle:

    def __init__(self, id):
        self.__id = id

    def getId(self):
        return self.__id

    def getCurrentPosition(self):
        return traci.vehicle.getPosition(self.__id)

    def getAcceleration(self):
        return traci.vehicle.getAcceleration(self.__id)

    def getEmissions(self):
        return traci.vehicle.getCO2Emission(self.__id)

    def getNextTrafficLight(self):
        return traci.vehicle.getNextTLS(self.__id)

    def isOnTrack(self):
        return isVehicleKnown(self.getId())

    def isStopped(self):
        return self.getAcceleration() == 0 and self.getSpeed() == 0

    def isBreaking(self):
        return self.getAcceleration() < 0

    def isJammed(self):

        if not self.isStopped():
            return False

        follower = traci.vehicle.getFollower(self.__id)
        followerObject = AbstractVehicle
        leaderObject =  AbstractVehicle

        if follower:
            followerId = follower[0]
            followerObject = AbstractVehicle(followerId)
        leader = traci.vehicle.getLeader(self.__id)
        if leader:
            leaderId = leader[0]
            leaderObject = AbstractVehicle(leaderId)

        if followerObject.isOnTrack() and leaderObject.isOnStrack():
            return  followerObject.isStopped() and leaderObject.isStopped()
        
        if followerObject.isOnTrack():
            return  followerObject.isStopped()

        if leaderObject.isOnTrack():
            return  leaderObject.isStopped()

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
