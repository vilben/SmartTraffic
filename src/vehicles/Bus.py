import logging
from src.vehicles.AbstractVehicle import AbstractVehicle


class Bus(AbstractVehicle):

    def someAdditionalFunctionForBusses(self):
        logging.debug("yeet")
