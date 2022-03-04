from time import sleep
import sumolib
import traci

import src.util as util
import src.tlsControl as tlsControl
from src.vehicleControl import addBus, printVehicleTypes
from src.vehicles.Bus import Bus

SIM_STEPS = 500
WITH_GUI = False
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


print(traci.trafficlight.getIDList())

TLS_ID = "-1"
sguTls = tlsControl.TLSControl(TLS_ID, "111222333", "rrrrrrrrr")

printVehicleTypes()

vehs_at_tls = []

step = 0
while step < SIM_STEPS:
    traci.simulationStep()

    # print TLS state & sleep for 100ms
    # print("Step: {}".format(step))
    # print("TLS state: {}".format(traci.trafficlight.getRedYellowGreenState(TLS_ID)))
    # print("\n")
    # sguTls.set_state(traci.trafficlight.getRedYellowGreenState(TLS_ID))
    # sguTls.print_state()
    # sleep(0.1)

    # curr_vehs = util.getAllVehiclesAtTLS(TLS_ID)
    # for veh in curr_vehs:
    #     if veh not in vehs_at_tls:
    #         vehs_at_tls.append(veh)

    busId = addBus()

    bus = Bus(busId)

    upcomingRoute = bus.getUpcomingRoute()
    upcomingTls = bus.getAllUpcomingTrafficLightsInOrder()

    print(upcomingRoute)
    print(upcomingTls)

    step += 1

veh_stats = util.getVehicleStats(vehs_at_tls)
avg_veh_stats = util.getAvgVehicleStats(veh_stats)

# print vehicle statistics
print(f"Vehicle statistics for {len(vehs_at_tls)} vehicles :")
print("\n".join(["{}: {}".format(key, value) for key, value in avg_veh_stats.items()]))

traci.close()
