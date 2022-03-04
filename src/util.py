import traci


def getAllVehiclesAtTLS(tls_id):
    """
    Returns a list of vehicle IDs that pass the given traffic light.
    """
    ids = traci.vehicle.getIDList()
    vehs = []
    for id in ids:
        for lst in traci.vehicle.getNextTLS(id):
            if tls_id in lst:
                vehs.append(id)
    return vehs


def getVehicleStats(veh_ids):
    """
    Returns a list of dictionaries containing the statistics of the given vehicles.
    """
    veh_stats = []
    for veh_id in veh_ids:
        try:
            veh_stats.append(
                {
                    "id": veh_id,
                    "co2": traci.vehicle.getCO2Emission(veh_id),
                    "co": traci.vehicle.getCOEmission(veh_id),
                    "hc": traci.vehicle.getHCEmission(veh_id),
                }
            )
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
    avg_veh_stats["co2"] /= len(veh_stats)
    avg_veh_stats["co"] /= len(veh_stats)
    avg_veh_stats["hc"] /= len(veh_stats)
    return avg_veh_stats


def getAllTlsIds():
    """
    Returns a list of all traffic light IDs.
    """
    return traci.trafficlight.getIDList()
