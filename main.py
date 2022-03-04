from time import sleep
import sumolib
import traci

import src.util as util
import src.tlsControl as tlsControl
from src.vehicleControl import addBus, printVehicleTypes, setRandomVehicleColor

SIM_STEPS = 5000
WITH_GUI = True
VIEW_ID = "View #0"
ZOOM_LVL = 2000
# CENTER_X, CENTER_Y = 4577.56, 4533.25
CENTER_X, CENTER_Y = 4912.04, 3512.10

if WITH_GUI:
    sumoBinary = sumolib.checkBinary("sumo-gui")
else:
    sumoBinary = sumolib.checkBinary("sumo")

cmd = [sumoBinary, "-c", "config/lucerne.sumo.cfg"]

traci.start(cmd)

# if WITH_GUI:
#     traci.gui.setZoom(VIEW_ID, ZOOM_LVL)
#     traci.gui.setOffset(VIEW_ID, CENTER_X, CENTER_Y)


print(f'TLS: {traci.trafficlight.getIDList()}')
print(f'Junctions: {traci.junction.getIDList()}')


TLS_ID = "10"
sguTls = tlsControl.TLSControl(TLS_ID, "111222333", "rrrrrrrrr")
# sguTls.print_state()
# print("setting first light, second and third to green")
# sguTls.set("1", 1, "g")
# sguTls.set("1", 2, "g")
# sguTls.print_state()
# print("setting 3rd light, 0 and 1 to G")
# sguTls.set("3", 0, "G")
# sguTls.set("3", 1, "G")
# sguTls.print_state()

printVehicleTypes()

vehs_at_tls = []

step = 0
while step < SIM_STEPS:
    traci.simulationStep()

    if step % 10 == 0:
        addBus()

    # setRandomVehicleColor(util.getRandomColor())

    curr_vehs = util.getAllVehiclesAtTLS(TLS_ID)
    for veh in curr_vehs:
        if veh not in vehs_at_tls:
            vehs_at_tls.append(veh)

    step += 1

veh_stats = util.getVehicleStats(vehs_at_tls)
avg_veh_stats = util.getAvgVehicleStats(veh_stats)

# print vehicle statistics
print(f"Vehicle statistics for {len(vehs_at_tls)} vehicles :")
print("\n".join(["{}: {}".format(key, value) for key, value in avg_veh_stats.items()]))

traci.close()
