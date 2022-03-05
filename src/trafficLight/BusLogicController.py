import logging
import src.trafficLight.JunctionController


class BusLogicController:
    def __init__(self, junctionManager):
        self.allBusses = []
        self.junctionManager = junctionManager
        self.approaches = {}

    @property
    def junctionManager(self) -> src.trafficLight.JunctionController.JunctionManager:
        return self._junctionManager

    @junctionManager.setter
    def junctionManager(self, junctionManager):
        self._junctionManager = junctionManager

    def addBus(self, bus):
        self.allBusses.append(bus)

    def addBusRange(self, busses):
        self.allBusses.extend(busses)

    def executeLogic(self):
        for bus, tlsId in self.approaches.items():
            nextTls = bus.getNextTrafficLight()
            junctionControl = self.junctionManager.getJunctionControl(
                self.approaches[bus]
            )
            if nextTls is None:
                junctionControl.declareInactive(self, bus.getId())
                junctionControl.releaseJunction(bus.getId())
                logging.debug(
                    f"Removed bus {bus.getId()} from approach as it does not appear to have a lane"
                )
            elif nextTls.getId() != tlsId:
                junctionControl.declareInactive(bus.getId())
                junctionControl.releaseJunction(bus.getId())
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
                    distance = 51

                if distance < 50 or bus.isJammed():
                    if not bus.hasBusStopAheadOnSameLane() or bus.isJammed():
                        tls = bus.getNextTrafficLight()
                        logging.debug(f"Bus {bus.getId()} is approaching {tls.getId()}")
                        if tls is not None:
                            self.declareBusApproachingTls(bus, tls.getId())
                            junctionControl = self.junctionManager.getJunctionControl(
                                tls.getId()
                            )
                            if junctionControl.isOwner(
                                bus.getId()
                            ) or junctionControl.acquireJunction(bus.getId()):
                                tls.ensureAccess()
                                logging.debug("Changing light because bus is jammed!!")
                            else:
                                junctionControl.declareActive(
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
