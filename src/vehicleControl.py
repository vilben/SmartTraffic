from cgitb import text
import logging
import random
import uuid
import traci


def __getRandomId() -> text:
    """
    Returns a random ID.
    """
    return str(uuid.uuid4())


def addBus() -> text:
    """
    Adds a bus to the simulation.
    Returns the ID of the bus.
    """
    id = __getRandomId()
    traci.vehicle.add(id, "", typeID="DEFAULT_VEHTYPE", personCapacity=25)
    traci.vehicle.setVehicleClass(id, "bus")
    traci.vehicle.setShapeClass(id, "bus")
    traci.vehicle.setColor(id, (255, 0, 0, 255))
    return id

def setVehicleColor(id, color):
    """
    Sets the color of the given vehicle.
    """
    traci.vehicle.setColor(id, color)

def setRandomVehicleColor(color) -> text:
    """
    Sets a random vehicle's color.
    """
    id = getRandomVehicle()
    setVehicleColor(id, color)
    return id

def getRandomVehicle() -> text:
    """
    Returns a random vehicle.
    """
    vehicleList = traci.vehicle.getIDList()
    return vehicleList[random.randint(0, len(vehicleList) - 1)]


def logVehicleTypes():
    """
    Prints all vehicle types.
    """
    logging.info(traci.vehicletype.getIDList())

def followVehicleWithGUI(vehicleId, viewId):
    """
    Follows the given vehicle with the given GUI.
    """
    pos = traci.vehicle.getPosition(vehicleId)
    traci.gui.setOffset(viewId, pos[0], pos[1])

def isVehicleKnown(vehicleId):
    """
    Returns whether the given vehicle is known.
    """
    return vehicleId in traci.vehicle.getIDList()