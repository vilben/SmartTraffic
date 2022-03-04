import sumolib
import traci

import src.util as util
import src.tlsControl as tlsControl
from src.vehicles.Bus import Bus
from src.vehicleControl import addBus, printAllvTypes, printVehicleTypes, setRandomVehicleColor

SIM_STEPS = 5000
WITH_GUI = True
VIEW_ID = "View #0"
ZOOM_LVL = 2000
# CENTER_X, CENTER_Y = 4577.56, 4533.25
CENTER_X, CENTER_Y = 4912.04, 3512.10
CONFIG_FILE_NAME = "config/lucerne.sumo.cfg"

if WITH_GUI:
    sumoBinary = sumolib.checkBinary("sumo-gui")
else:
    sumoBinary = sumolib.checkBinary("sumo")

cmd = [sumoBinary, "-c", CONFIG_FILE_NAME]
traci.start(cmd)


print(f"TLS: {traci.trafficlight.getIDList()}")
print(f"Junctions: {traci.junction.getIDList()}")
printAllvTypes()

TLS_ID = "10"
sguTls = tlsControl.TLSControl(TLS_ID, "111222333", "rrrrrrrrr")

vehStats = {}
busStats = {}
printVehicleTypes()

vehs_at_tls = []
allBusses = []

step = 0
while step < SIM_STEPS:
    traci.simulationStep()

    if step % 10 == 0:
        printAllvTypes()
        busId = addBus()
        bus = Bus(busId)
        allBusses.append(bus)

    for busId in util.getAllVehiclesOfClass("bus"):
        busStats[busId] = util.getSingleVehilceStats(busId)

    for vehId in util.getAllVehilcesExcept("bus"):
        vehStats[vehId] = util.getSingleVehilceStats(vehId)

    for bus in allBusses:

        if bus.isOnTrack():

            print("bus no ", bus.getId(), " drives on route:")
            print(bus.getUpcomingRoute())
            print("on this route, the upcoming traffic lights are:")
            print(bus.getAllUpcomingTrafficLightsInOrder())
            print("")

    print("---- next step ----")
    step += 1

avgVehStats = util.getAvgVehicleStats(vehStats.values())
totalVehStats = util.getTotalVehicleStats(vehStats.values())
avgBusStats = util.getAvgVehicleStats(busStats.values())
totalBusStats = util.getTotalVehicleStats(busStats.values())

# print vehicle statistics
print(f"Vehicle statistics for {len(vehStats)} vehicles (avg, tot) :")
print("\n".join(["{}: {}".format(key, value) for key, value in avgVehStats.items()]))
print("\n")
print("\n".join(["{}: {}".format(key, value) for key, value in totalVehStats.items()]))
print("\n")
print("\n")
print(f"\nBus statistics for {len(busStats)} vehicles (avg, tot) :")
print("\n".join(["{}: {}".format(key, value) for key, value in avgBusStats.items()]))
print("\n")
print("\n".join(["{}: {}".format(key, value) for key, value in totalBusStats.items()]))

traci.close()
