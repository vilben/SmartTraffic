from time import sleep
import sumolib
import traci

import src.util as util
import src.tlsControl as tlsControl
from src.vehicles.Bus import Bus
from src.vehicleControl import addBus, printVehicleTypes, setRandomVehicleColor

SIM_STEPS = 500
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

printVehicleTypes()

vehs_at_tls = []
allBusses = []

step = 0
while step < SIM_STEPS:
    traci.simulationStep()

    if step % 10 == 0:
        busId = addBus()

        bus = Bus(busId)

        allBusses.append(bus)

    setRandomVehicleColor(util.getRandomColor())

    step += 1

    print("upcoming routes")
    print(allBusses[0].getUpcomingRoute())
    print("upcoming tls")
    print(allBusses[0].getAllUpcomingTrafficLightsInOrder())

veh_stats = util.getVehicleStats(vehs_at_tls)
avg_veh_stats = util.getAvgVehicleStats(veh_stats)

# print vehicle statistics
print(f"Vehicle statistics for {len(vehs_at_tls)} vehicles :")
print("\n".join(["{}: {}".format(key, value) for key, value in avg_veh_stats.items()]))

traci.close()
