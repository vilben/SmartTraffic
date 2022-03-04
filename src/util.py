from distutils.log import error
import random
import traci


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
            # else:
            # print(f"{veh_id} is not of class {vehicleClass}, its {traci.vehicle.getVehicleClass(veh_id)}")
        except:
            pass
    return veh_stats


def getAvgVehicleStats(veh_stats):
    """
    Returns a dictionary containing the average statistics of the given vehicles.
    """
    avg_veh_stats = {
        "co2": 0,
        "co": 0,
        "hc": 0,
    }
    for veh_stat in veh_stats:
        avg_veh_stats["co2"] += veh_stat["co2"]
        avg_veh_stats["co"] += veh_stat["co"]
        avg_veh_stats["hc"] += veh_stat["hc"]
    avg_veh_stats["co2"] /= max(len(veh_stats), 1)
    avg_veh_stats["co"] /= max(len(veh_stats), 1)
    avg_veh_stats["hc"] /= max(len(veh_stats), 1)
    return avg_veh_stats


def printAllTlsStates():
    for tls_id in traci.trafficlight.getIDList():
        print(f"{tls_id}:  {traci.trafficlight.getRedYellowGreenState(tls_id)}")


def getRandomColor():
    return (
        int(random.random() * 255),
        int(random.random() * 255),
        int(random.random() * 255),
    )
