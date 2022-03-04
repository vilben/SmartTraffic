import sumolib
import traci

import src.util as util
from src.vehicleControl import addBus, printAllvTypes

SIM_STEPS = 500
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

vehStats = {}
busStats = {}

step = 0
while step < SIM_STEPS:
    traci.simulationStep()

    if step % 10 == 0:
        printAllvTypes()
        busId = addBus()

    for busId in util.getAllVehiclesOfClass("bus"):
        busStats[busId] = util.getSingleVehilceStats(busId)

    for vehId in util.getAllVehilcesExcept("bus"):
        vehStats[vehId] = util.getSingleVehilceStats(vehId)

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
