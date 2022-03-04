import argparse
import logging

import sumolib
import traci

import src.util as util
import src.tlsControl as tlsControl
from src.vehicles.Bus import Bus
from src.vehicleControl import (
    addBus,
    printVehicleTypes,
    setRandomVehicleColor,
)

#
# Setup of stuff
#

SIM_STEPS = 5000
VIEW_ID = "View #0"
CONFIG_FILE_NAME = "config/lucerne.sumo.cfg"

parser = argparse.ArgumentParser(description='Yes something')
parser.add_argument('--GUI', action='store_true', help='Define if GUI should be used')
parser.add_argument('--DEBUG', action='store_true', help='Define if DEBUG should be used')

args = parser.parse_args()

DEBUG = args.DEBUG
GUI = args.GUI

if GUI:
    sumoBinary = sumolib.checkBinary("sumo-gui")
else:
    sumoBinary = sumolib.checkBinary("sumo")


if DEBUG:
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
else:
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

cmd = [sumoBinary, "-c", CONFIG_FILE_NAME]
traci.start(cmd)

vehStats = {}
busStats = {}

vehs_at_tls = []
allBusses = []

step = 0
while step < SIM_STEPS:
    traci.simulationStep()

    if step % 10 == 0:
        busId = addBus()
        bus = Bus(busId)
        allBusses.append(bus)

    for busId in util.getAllVehiclesOfClass("bus"):
        busStats[busId] = util.getSingleVehilceStats(busId)

    for vehId in util.getAllVehilcesExcept("bus"):
        vehStats[vehId] = util.getSingleVehilceStats(vehId)

    for bus in allBusses:
        if bus.isOnTrack():
            logging.debug("bus no {0} drives on route {1} \n on this route, the upcoming traffic lights are: \n {2}".format(bus.getId(), bus.getUpcomingRoute(), bus.getAllUpcomingTrafficLightsInOrder()))
    
    logging.debug("---- next step ----")
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
