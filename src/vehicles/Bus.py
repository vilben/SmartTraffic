from src.vehicles.Vehicle import AbstractVehicle


class Bus(AbstractVehicle):

    def getNextBusStop(self):
        nextStop = self.getNextStop()
        n = 2
        while not nextStop.isBusStop() and n < 100:
            nextStop = self.getNthNextStop(n)
            n += 1
            
        return nextStop

    def hasBusStopAheadOnSameLane(self):

        currentLane = self.getCurrentLane()
        nextBusStopLane = self.getNextBusStop().getLane()

        return currentLane == nextBusStopLane
