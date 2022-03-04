from cgitb import text
import uuid
import traci


def __get_random_id() -> text:
    """
    Returns a random ID.
    """
    return str(uuid.uuid4())


def add_bus() -> text:
    """
    Adds a bus to the simulation.
    Returns the ID of the bus.
    """
    id = __get_random_id()
    traci.vehicle.add(id, "", typeID="veh_passenger", personCapacity=25)
    traci.vehicle.setVehicleClass(id, "bus")
    traci.vehicle.setColor(id, (255, 0, 0, 255))
    return id


def print_vehicle_types():
    """
    Prints all vehicle types.
    """
    print(traci.vehicletype.getIDList())
