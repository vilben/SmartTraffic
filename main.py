import argparse
import logging
import sumolib
import traci

import src.util as util
from src import tlsControl
from src.vehicles.Bus import Bus
from src.vehicleControl import addBus

VIEW_ID = "View #0"
ENABLE_STATS = False
CONFIG_FILE_NAME = "config/lucerne.sumo.cfg"

parser = argparse.ArgumentParser(description="Yes something")
parser.add_argument(
    "--GUI", action="store_true", help="Define if GUI should be used"
)
parser.add_argument(
    "--DEBUG", action="store_true", help="Define if DEBUG should be used"
)
parser.add_argument(
    "--STATS", action="store_true", help="Define if STATS should be generated"
)
parser.add_argument(
    '--STEPS', type=int, default=5000, help="Define maximal simulation steps"
)

args = parser.parse_args()

SIM_STEPS = args.STEPS
DEBUG = args.DEBUG
GUI = args.GUI
STATS = args.STATS

if GUI:
    sumoBinary = sumolib.checkBinary("sumo-gui")
else:
    sumoBinary = sumolib.checkBinary("sumo")

if DEBUG:
    logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.DEBUG,
    )
else:
    logging.basicConfig(
        format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
    )

cmd = [sumoBinary, "-c", CONFIG_FILE_NAME]
traci.start(cmd)

vehStats = {}
busStats = {}

vehs_at_tls = []
allBusses = [Bus("busRouteHorwLuzern1"), Bus("busRouteHorwLuzern2"), Bus("busRouteEmmenAu1"), Bus("busRouteEmmenAu1"),
             Bus("busRouteEmmenAu1"), Bus("busRouteEmmenAu2"), Bus("busRouteWuerzenbachZug1"),
             Bus("busRouteWuerzenbachZug2"), Bus("busRouteEbikonHorw1"), Bus("busRouteEbikonHorw2"),
             Bus("busRouteZugHorw1"), Bus("busRouteZugHorw2")]

step = 0
while step < SIM_STEPS:
    traci.simulationStep()

    for bus in allBusses:

        if bus.isOnTrack():
            logging.debug(f'bus {bus}')
            tls = bus.getNextTrafficLight()[0]

            tlsId = tls[0]
            tlsPhase = tls[3]

            # just skip stupid phases...
            if tlsPhase == 'r' or tlsPhase == 'R' or tlsPhase == 'y' or tlsPhase == 'Y':
                traci.trafficlight.setPhaseDuration(tlsId, 0)

    if STATS:
        for busId in util.getAllVehiclesOfClass("bus"):
            busStats[busId] = util.getSingleVehilceStats(busId)

        for vehId in util.getAllVehilcesExcept("bus"):
            vehStats[vehId] = util.getSingleVehilceStats(vehId)

    logging.debug("---- next step ----")
    step += 1

if STATS:
    avgVehStats = util.getAvgVehicleStats(vehStats.values())
    totalVehStats = util.getTotalVehicleStats(vehStats.values())
    avgBusStats = util.getAvgVehicleStats(busStats.values())
    totalBusStats = util.getTotalVehicleStats(busStats.values())

    # print vehicle statistics
    print(f"Vehicle statistics for {len(vehStats)} vehicles (avg, tot) :")
    print(
        "\n".join(["{}: {}".format(key, value) for key, value in avgVehStats.items()])
    )
    print("\n")
    print(
        "\n".join(["{}: {}".format(key, value) for key, value in totalVehStats.items()])
    )
    print("\n")
    print("\n")
    print(f"\nBus statistics for {len(busStats)} vehicles (avg, tot) :")
    print(
        "\n".join(["{}: {}".format(key, value) for key, value in avgBusStats.items()])
    )
    print("\n")
    print(
        "\n".join(["{}: {}".format(key, value) for key, value in totalBusStats.items()])
    )

traci.close()
