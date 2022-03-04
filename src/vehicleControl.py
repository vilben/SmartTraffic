from cgitb import text
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
    traci.vehicle.add(id, "", typeID="veh_passenger", personCapacity=25)
    traci.vehicle.setVehicleClass(id, "bus")
    traci.vehicle.setColor(id, (255, 0, 0, 255))
    return id


def printVehicleTypes():
    """
    Prints all vehicle types.
    """
    print(traci.vehicletype.getIDList())
