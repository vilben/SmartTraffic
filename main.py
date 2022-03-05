import argparse
import logging
import time
import sumolib
import traci
from src.edgeStats import EdgeStatsCollector

from src.vehicles.Bus import Bus
from src.trafficLight.BusLogicController import BusLogicController
from src.trafficLight.JunctionMutexFactory import JunctionMutexFactory

VIEW_ID = "View #0"
ENABLE_STATS = False
#CONFIG_FILE_NAME = "config/lucerne.sumo.cfg"
CONFIG_FILE_NAME = "lucerne-real/osm.sumocfg"

parser = argparse.ArgumentParser(description="Yes something")

parser.add_argument(
    "--GUI", 
    action="store_true", 
    help="Define if GUI should be used"
)
parser.add_argument(
    "--DEBUG", 
    action="store_true", 
    help="Define if DEBUG should be used"
)
parser.add_argument(
    "--STEPS", 
    type=int,
    default=5000, 
    help="Define maximal simulation steps"
)
parser.add_argument(
    "--DIAGS",
    action="store_true",
    help="Enable Diagram creation",
)
parser.add_argument(
    "--JSON",
    action="store_true",
    help="Enable JSON creation",
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
parser.add_argument(
    "--SPLUNKDATASETNAME",
    type=str,
    help="Splunk Dataset Name",
)
parser.add_argument(
    "--DISTANCE",
    type=int,
    default=50,
    help="distance",
)

args = parser.parse_args()

SIM_STEPS = args.STEPS
DEBUG = args.DEBUG
GUI = args.GUI
DIAGS = args.DIAGS
JSON = args.JSON
SPLUNK = args.SPLUNK
DISTANCE = args.DISTANCE
SPLUNKTOKEN = args.SPLUNKTOKEN
SPLUNKDEST = args.SPLUNKDEST
SPLUNKDATASETNAME = args.SPLUNKDATASETNAME
TIMESTAMP = time.time()
SIMID = f"{TIMESTAMP}_{SPLUNKDATASETNAME}"

COLLECT_DATA = DIAGS or JSON or SPLUNK

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

logging.info(f"SIM-ID: {SIMID}")

cmd = [sumoBinary, "-c", CONFIG_FILE_NAME]
traci.start(cmd)

junctionMutexFactory = JunctionMutexFactory()

# allBusses = [
#     Bus("busRouteHorwLuzern1"),
#     Bus("busRouteHorwLuzern2"),
#     Bus("busRouteEmmenAu1"),
#     Bus("busRouteEmmenAu1"),
#     Bus("busRouteEmmenAu1"),
#     Bus("busRouteEmmenAu2"),
#     Bus("busRouteWuerzenbachZug1"),
#     Bus("busRouteWuerzenbachZug2"),
#     Bus("busRouteEbikonHorw1"),
#     Bus("busRouteEbikonHorw2"),
#     Bus("busRouteZugHorw1"),
#     Bus("busRouteZugHorw2"),
# ]

allBusses = []
for i in range(0, 1852):
    allBusses.append(Bus("bus{}".format(i)))

busLogicController = BusLogicController(junctionMutexFactory, DISTANCE)
busLogicController.addBusRange(allBusses)

step = 0
if COLLECT_DATA:
    edgeStatsCollector = EdgeStatsCollector(SIM_STEPS, "diags", "json", SIMID)
    edgeStatsCollector.registerAllRelevantEdges()

while step < SIM_STEPS:
    traci.simulationStep()
    busLogicController.executeLogic()

    if COLLECT_DATA:
        edgeStatsCollector.collect(step)

    print("Step No.", step)

    if step > 1000:
        if traci.vehicle.getIDCount() < len(allBusses):
            logging.info(f"Step: {step}, Simulation finished!")
            logging.info(f"==================================================")
            break
    step += 1

if DIAGS:
    edgeStatsCollector.createDiags()
if JSON:
    edgeStatsCollector.writeJSON()
if SPLUNK:
    edgeStatsCollector.sendJsonToSplunk(SPLUNKDEST, SPLUNKTOKEN)

traci.close()
