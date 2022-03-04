from distutils.log import error
import traci
import random


def getAllVehiclesAtTLS(tls_id, vehicleClass=""):
    """
    Returns a list of vehicle IDs that pass the given traffic light.
    """
    ids = traci.vehicle.getIDList()
    vehs = []
    for id in ids:
        for lst in traci.vehicle.getNextTLS(id):
            if tls_id in lst:
                if (
                    vehicleClass == ""
                    or traci.vehicle.getVehicleClass(id) == vehicleClass
                ):
                    vehs.append(id)
    return vehs


def getAllVehiclesOfClass(vehicleClass):
    """
    Returns a list of all vehicles of the given class.
    """
    ids = traci.vehicle.getIDList()
    vehs = []
    for id in ids:
        if traci.vehicle.getVehicleClass(id) == vehicleClass:
            vehs.append(id)
    return vehs


def getAllVehilcesExcept(vehicleClass):
    """
    Returns a list of all vehicles except the given class.
    """
    ids = traci.vehicle.getIDList()
    vehs = []
    for id in ids:
        if traci.vehicle.getVehicleClass(id) != vehicleClass:
            vehs.append(id)
    return vehs


def getSingleVehilceStats(veh_id):
    """
    Returns a dictionary containing the statistics of the given vehicle.
    """
    veh_stats = {
        "id": veh_id,
        "co2": traci.vehicle.getCO2Emission(veh_id),
        "co": traci.vehicle.getCOEmission(veh_id),
        "hc": traci.vehicle.getHCEmission(veh_id),
        "distance": traci.vehicle.getDistance(veh_id),
        "nOfPeople": traci.vehicle.getPersonNumber(
            veh_id
        ),  # this is currently not working... (?)
    }
    return veh_stats


def getVehicleStats(veh_ids, vehicleClass=""):
    """
    Returns a list of dictionaries containing the statistics of the given vehicles.
    """
    veh_stats = []
    for veh_id in veh_ids:
        try:
            if (
                vehicleClass == ""
                or traci.vehicle.getVehicleClass(veh_id) == vehicleClass
            ):
                veh_stats.append(getSingleVehilceStats(veh_id))
        except:
            pass
    return veh_stats


def getAvgVehicleStats(vehStats):
    """
    Returns a dictionary containing the average statistics of the given vehicles.
    """
    avg_veh_stats = {
        "co2": 0,
        "co": 0,
        "hc": 0,
        "distance": 0,
        "nOfPeople": 0,
    }
    for veh_stat in vehStats:
        avg_veh_stats["co2"] += veh_stat["co2"]
        avg_veh_stats["co"] += veh_stat["co"]
        avg_veh_stats["hc"] += veh_stat["hc"]
        avg_veh_stats["distance"] += veh_stat["distance"]
        avg_veh_stats["nOfPeople"] += veh_stat["nOfPeople"]
    avg_veh_stats["co2"] /= max(len(vehStats), 1)
    avg_veh_stats["co"] /= max(len(vehStats), 1)
    avg_veh_stats["hc"] /= max(len(vehStats), 1)
    avg_veh_stats["distance"] /= max(len(vehStats), 1)
    avg_veh_stats["nOfPeople"] /= max(len(vehStats), 1)
    return avg_veh_stats


def getTotalVehicleStats(vehStats):
    """
    Returns a dictionary containing the total statistics of the given vehicles.
    """
    total_veh_stats = {
        "co2": 0,
        "co": 0,
        "hc": 0,
        "distance": 0,
        "nOfPeople": 0,
    }
    for veh_stat in vehStats:
        total_veh_stats["co2"] += veh_stat["co2"]
        total_veh_stats["co"] += veh_stat["co"]
        total_veh_stats["hc"] += veh_stat["hc"]
        total_veh_stats["distance"] += veh_stat["distance"]
        total_veh_stats["nOfPeople"] += veh_stat["nOfPeople"]
    return total_veh_stats


def printAllTlsStates():
    for tls_id in traci.trafficlight.getIDList():
        print(f"{tls_id}:  {traci.trafficlight.getRedYellowGreenState(tls_id)}")


def getRandomColor():
    return (
        int(random.random() * 255),
        int(random.random() * 255),
        int(random.random() * 255),
    )