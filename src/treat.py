import traci

def get_veh_ids_at_tls(tls_id):
    """
    Returns a list of vehicle IDs that pass the given traffic light.
    """
    tls_edges = traci.trafficlight.getControlledLinks(tls_id)
    tls_edges = [edge for sublist in tls_edges for edge in sublist]
    veh_ids = traci.vehicle.getIDList()
    veh_ids_at_tls = []
    for veh_id in veh_ids:
        veh_edge = traci.vehicle.getRoadID(veh_id)
        if veh_edge in tls_edges:
            veh_ids_at_tls.append(veh_id)
        else:
            veh_ids_at_tls.append(veh_id)
    return veh_ids_at_tls

def get_veh_stats(veh_ids):
    """
    Returns a list of dictionaries containing the statistics of the given vehicles.
    """
    veh_stats = []
    for veh_id in veh_ids:
        veh_stats.append({
            'id': veh_id,
            'co2': traci.vehicle.getCO2Emission(veh_id),
            'co': traci.vehicle.getCOEmission(veh_id),
            'hc': traci.vehicle.getHCEmission(veh_id),
        })
    return veh_stats

def get_avg_veh_stats(veh_stats):
    """
    Returns a dictionary containing the average statistics of the given vehicles.
    """
    avg_veh_stats = {
        'co2': 0,
        'co': 0,
        'hc': 0,
    }
    for veh_stat in veh_stats:
        avg_veh_stats['co2'] += veh_stat['co2']
        avg_veh_stats['co'] += veh_stat['co']
        avg_veh_stats['hc'] += veh_stat['hc']
    avg_veh_stats['co2'] /= len(veh_stats)
    avg_veh_stats['co'] /= len(veh_stats)
    avg_veh_stats['hc'] /= len(veh_stats)
    return avg_veh_stats