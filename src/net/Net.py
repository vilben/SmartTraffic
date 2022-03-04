import sumolib
import logging


class Net:
    def __init__(self):
        try:
            self.__net = sumolib.net.readNet("nets/lucerne.net.xml")
        except Exception as e:
            logging.error("no idea how to handle exceptions in snake", e)

    def getNet(self):
        return self.__net

    def getNodeIdOfEdge(self, edgeId):
        return self.__net.getEdge(edgeId).getToNode().getID()
