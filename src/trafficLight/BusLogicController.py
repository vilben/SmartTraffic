import logging
from src.trafficLight.JunctionMutexFactory import JunctionMutexFactory


class BusLogicController:
    def __init__(self, junctionMutexFactory, distance):
        self.allBusses = []
        self.junctionMutexFactory = junctionMutexFactory
        self.approaches = {}
        self.__distance = distance

    @property
    def junctionMutexFactory(self) -> JunctionMutexFactory:
        return self._junctionManager

    @junctionMutexFactory.setter
    def junctionMutexFactory(self, junctionMutexFactory):
        self._junctionManager = junctionMutexFactory

    def addBus(self, bus):
        self.allBusses.append(bus)

    def addBusRange(self, busses):
        self.allBusses.extend(busses)

    def executeLogic(self):
        for bus, tlsId in self.approaches.items():
            nextTls = bus.getNextTrafficLight()
            junctionMutex = self.junctionMutexFactory.getJunctionMutex(
                self.approaches[bus]
            )
            if nextTls is None:
                junctionMutex.declareInactive(bus.getId())
                junctionMutex.releaseJunction(bus.getId())
                logging.debug(
                    f"Removed bus {bus.getId()} from approach as it does not appear to have a lane"
                )
            elif nextTls.getId() != tlsId:
                junctionMutex.declareInactive(bus.getId())
                junctionMutex.releaseJunction(bus.getId())
                self.approaches[bus] = nextTls.getId()
                logging.debug(
                    f"Removed bus {bus.getId()} from approach as it has left its approaching lane"
                )
            else:
                logging.debug(f"Keeping bus {bus.getId()} on approach")

        for bus in self.allBusses:
            if bus.isOnTrack():
                try:
                    distance = bus.getNextTrafficLight().getDistanceFromVehicle()
                except Exception as e:
                    distance = self.__distance + 1

                if distance < self.__distance or bus.isJammed():
                    nextTrafficLight = bus.getNextTrafficLight()
                    if nextTrafficLight.isControllingLane(bus.getCurrentLane()):
                        if not bus.hasBusStopAheadOnSameLane() or bus.isJammed():
                            logging.debug(f"Bus {bus.getId()} is approaching {nextTrafficLight.getId()}")
                            if nextTrafficLight is not None:
                                self.declareBusApproachingTls(bus, nextTrafficLight.getId())
                                junctionMutex = self.junctionMutexFactory.getJunctionMutex(
                                    nextTrafficLight.getId()
                                )
                                if junctionMutex.isOwner(
                                    bus.getId()
                                ) or junctionMutex.acquireJunction(bus.getId()):
                                    nextTrafficLight.ensureAccess()
                                    logging.debug("Changing light because bus is jammed!!")
                                else:
                                    junctionMutex.declareActive(
                                        bus.getId(),
                                        "bus may have detected jammed traffic ahead",
                                        "",
                                        "",
                                    )
                                    logging.debug(
                                        f"Bus {bus.getId()} wants to clear junction, but other busses appear to have priority"
                                    )

    def declareBusApproachingTls(self, bus, tlsId):
        self.approaches[bus] = tlsId
