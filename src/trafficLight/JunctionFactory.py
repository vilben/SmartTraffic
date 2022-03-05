from trafficLight.JunctionMutex import JunctionMutex


class JunctionMutexFactory:
    def __init__(self):
        self.junctionMutexes = {}

    def getJunctionMutex(self, tlsId):
        if tlsId not in self.junctionMutexes:
            self.junctionMutexes[tlsId] = JunctionMutex(tlsId)

        return self.junctionMutexes[tlsId]
