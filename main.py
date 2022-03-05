import argparse
import logging
import uuid
import sumolib
import traci
from src.edgeStats import EdgeStatsCollector

from src.vehicles.Bus import Bus

VIEW_ID = "View #0"
ENABLE_STATS = False
CONFIG_FILE_NAME = "config/lucerne.sumo.cfg"

parser = argparse.ArgumentParser(description="Yes something")
parser.add_argument("--GUI", action="store_true", help="Define if GUI should be used")
parser.add_argument(
    "--DEBUG", action="store_true", help="Define if DEBUG should be used"
)
parser.add_argument(
    "--STEPS", type=int, default=5000, help="Define maximal simulation steps"
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

args = parser.parse_args()

SIM_STEPS = args.STEPS
DEBUG = args.DEBUG
GUI = args.GUI
DIAGS = args.DIAGS
SIMID = str(uuid.uuid4())
JSON = args.JSON
SPLUNK = args.SPLUNK
SPLUNKTOKEN = args.SPLUNKTOKEN
SPLUNKDEST = args.SPLUNKDEST

logging.info(f"SIM-ID: {SIMID}")

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

cmd = [sumoBinary, "-c", CONFIG_FILE_NAME]
traci.start(cmd)

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
if COLLECT_DATA:
    edgeStatsCollector = EdgeStatsCollector(SIM_STEPS, "diags", "json", SIMID)

    allEdges = traci.edge.getIDList()
    for edgeId in allEdges:
        edgeStatsCollector.registerEdge(edgeId)

while step < SIM_STEPS:
    traci.simulationStep()

    if COLLECT_DATA:
        edgeStatsCollector.collect(step)

    for bus in allBusses:
        if bus.isOnTrack():

            try:
                distance = bus.getNextTrafficLight().getDistanceFromVehicle()
            except Exception as e:
                distance = 51
                if DEBUG:
                    logging.debug(e)

            if (
                    distance < 50
                    or bus.isJammed()
            ):
                if not bus.hasBusStopAheadOnSameLane() or bus.isJammed():
                    tls = bus.getNextTrafficLight()
                    if tls is not None:
                        tls.setToGreen()
                        logging.debug("Changing light because bus is jammed!!")

    logging.debug(f"---- finished step {step} ----")
    step += 1

if DIAGS:
    edgeStatsCollector.createDiags()
if JSON:
    edgeStatsCollector.writeJSON()
if SPLUNK:
    edgeStatsCollector.sendJsonToSplunk(SPLUNKDEST, SPLUNKTOKEN)

traci.close()
