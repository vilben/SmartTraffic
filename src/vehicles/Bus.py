import logging
from src.vehicles.Vehicle import AbstractVehicle


class Bus(AbstractVehicle):

    def someAdditionalFunctionForBusses(self):
        logging.debug("yeet")
