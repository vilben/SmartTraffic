import argparse
import logging
from matplotlib.pyplot import text
import sumolib
import traci
from src.edgeStats import EdgeStatsCollector

import src.util as util
from src.vehicles.Bus import Bus
from src.vehicleControl import followVehicleWithGUI

VIEW_ID = "View #0"
ENABLE_STATS = False
CONFIG_FILE_NAME = "config/lucerne.sumo.cfg"

parser = argparse.ArgumentParser(description="Yes something")
parser.add_argument("--GUI", action="store_true", help="Define if GUI should be used")
parser.add_argument(
    "--DEBUG", action="store_true", help="Define if DEBUG should be used"
)
parser.add_argument(
    "--STATS", action="store_true", help="Define if STATS should be generated"
)
parser.add_argument(
    "--STEPS", type=int, default=5000, help="Define maximal simulation steps"
)
parser.add_argument(
    "--DIAGS",
    action="store_true",
    help="Output folder for DIAGS. If ommited, no diags will be generated. Requires STATS",
)
parser.add_argument(
    "--DIAGNAMEPREFIX",
    type=str,
    help="Prefix for diag file name",
)
parser.add_argument(
    "--SPLUNK",
    action="store_true",
    help="Should data be sent to Splunk",
)
parser.add_argument(
    "--SPLUNKTOKEN",
    type=str,
    help="Splunk HEC Token",
)
parser.add_argument(
    "--SPLUNKDEST",
    type=str,
    help="Splunk HEC Collector",
)

args = parser.parse_args()

SIM_STEPS = args.STEPS
DEBUG = args.DEBUG
GUI = args.GUI
STATS = args.STATS
DIAGS = args.DIAGS
DIAGNAMEPREFIX = args.DIAGNAMEPREFIX
SPLUNK = args.SPLUNK
SPLUNKTOKEN = args.SPLUNKTOKEN
SPLUNKDEST = args.SPLUNKDEST

if GUI:
    sumoBinary = sumolib.checkBinary("sumo-gui")
else:
    sumoBinary = sumolib.checkBinary("sumo")

if DEBUG:
    logging.basicConfig(
        format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.DEBUG,
    )
else:
    logging.basicConfig(
        format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.INFO,
    )

cmd = [sumoBinary, "-c", CONFIG_FILE_NAME]
traci.start(cmd)

vehStats = {}
busStats = {}

vehs_at_tls = []
allBusses = [
    Bus("busRouteHorwLuzern1"),
    Bus("busRouteHorwLuzern2"),
    Bus("busRouteEmmenAu1"),
    Bus("busRouteEmmenAu1"),
    Bus("busRouteEmmenAu1"),
    Bus("busRouteEmmenAu2"),
    Bus("busRouteWuerzenbachZug1"),
    Bus("busRouteWuerzenbachZug2"),
    Bus("busRouteEbikonHorw1"),
    Bus("busRouteEbikonHorw2"),
    Bus("busRouteZugHorw1"),
    Bus("busRouteZugHorw2"),
]

step = 0
if STATS:
    edgeStatsCollector = EdgeStatsCollector(SIM_STEPS, DIAGNAMEPREFIX)

    allEdges = traci.edge.getIDList()
    for edgeId in allEdges:
        edgeStatsCollector.registerEdge(edgeId)

while step < SIM_STEPS:
    traci.simulationStep()

    for bus in allBusses:
        if bus.isOnTrack():
            if (
                bus.getNextTrafficLight().getDistanceFromVehicle() < 50
                or bus.isJammed()
            ):
                if not bus.hasBusStopAheadOnSameLane() or bus.isJammed():
                    tls = bus.getNextTrafficLight()
                    tls.setToGreen()
                    logging.debug("Changing light because bus is jammed!!")
                    # if GUI:
                        # followVehicleWithGUI(bus.getId(), VIEW_ID)

    if STATS:
        edgeStatsCollector.collect(step)
        for busId in util.getAllVehiclesOfClass("bus"):
            busStats[busId] = util.getSingleVehilceStats(busId)

        for vehId in util.getAllVehilcesExcept("bus"):
            vehStats[vehId] = util.getSingleVehilceStats(vehId)

    logging.debug("---- finished step {0} ----".format(str(step)))
    step += 1

if STATS:
    avgVehStats = util.getAvgVehicleStats(vehStats.values())
    totalVehStats = util.getTotalVehicleStats(vehStats.values())
    avgBusStats = util.getAvgVehicleStats(busStats.values())
    totalBusStats = util.getTotalVehicleStats(busStats.values())

    # print vehicle statistics
    logging.info(f"Vehicle statistics for {len(vehStats)} vehicles (avg, tot) :")
    logging.info(
        "\n".join(["{}: {}".format(key, value) for key, value in avgVehStats.items()])
    )
    logging.info("\n")
    logging.info(
        "\n".join(["{}: {}".format(key, value) for key, value in totalVehStats.items()])
    )
    logging.info("\n")
    logging.info("\n")
    logging.info(f"\nBus statistics for {len(busStats)} vehicles (avg, tot) :")
    logging.info(
        "\n".join(["{}: {}".format(key, value) for key, value in avgBusStats.items()])
    )
    logging.info("\n")
    logging.info(
        "\n".join(["{}: {}".format(key, value) for key, value in totalBusStats.items()])
    )

    if DIAGS:
        edgeStatsCollector.createDiags("diags")

    if SPLUNK:
        edgeStatsCollector.sendJsonToSplunk(SPLUNKDEST, SPLUNKTOKEN)

traci.close()
