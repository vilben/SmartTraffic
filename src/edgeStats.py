import errno
import json
import logging
import os
import requests
from urllib3.exceptions import InsecureRequestWarning

from src.xmlUtil import getJSONFromXML

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import traci
from matplotlib import pyplot as plt

from src.diagUtil import aggregateSeries


class EdgeStats:
    def __init__(self, edgeId, maxSimSteps, simId):
        self.edgeId = edgeId
        # index = simstep
        # [
        #    {
        #       "edgeId": edgeId,
        #       "": [
        #    }
        # ]
        self.dataPoints = [{}] * maxSimSteps
        self.maxSimSteps = maxSimSteps
        # self.aggrGroups = maxSimSteps // 10
        self.aggrGroups = 100
        self.seriesLength = self.aggrGroups
        self.simId = simId
        self.figSize = (20, 10)
        self.dpi = 300

    def createDatapoint(self, simStep):
        self.dataPoints[simStep] = {
            "edgeId": self.edgeId,
            "simId": self.simId,
            "simSteps": self.maxSimSteps,
            "simStep": simStep,
            "emissions": traci.edge.getCO2Emission(self.edgeId),
            "speed": traci.edge.getLastStepMeanSpeed(self.edgeId),
            "occupancy": traci.edge.getLastStepOccupancy(self.edgeId),
            "lastStepVehicleNumber": traci.edge.getLastStepVehicleNumber(self.edgeId),
            "lastStepHaltingNumber": traci.edge.getLastStepHaltingNumber(self.edgeId),
            "traveltime": traci.edge.getTraveltime(self.edgeId),
            "lastStepMeanSpeed": traci.edge.getLastStepMeanSpeed(self.edgeId),
            "lastStepOccupancy": traci.edge.getLastStepOccupancy(self.edgeId),
            "lastStepLength": traci.edge.getLastStepLength(self.edgeId),
            "Noise": traci.edge.getNoiseEmission(self.edgeId),
            "WaitingTime": traci.edge.getWaitingTime(self.edgeId),
            "FuelConsumption": traci.edge.getFuelConsumption(self.edgeId),
        }

    def writeJson(self, outputFolder):
        with open(os.path.join(outputFolder, f"{self.edgeId}.json"), "w") as f:
            json.dump(self.dataPoints, f)

    def serialize(self):
        return json.dumps(self.dataPoints)

    def createPlots(self, outputFolder):
        self.createSpeedPlot(outputFolder)
        self.createOccupancyPlot(outputFolder)
        self.createEmissionsPlot(outputFolder)
        # self.createTraveltimePlot(outputFolder)
        self.createVehicleNumberPlot(outputFolder)
        self.createHaltingNumberPlot(outputFolder)
        self.createNoisePlot(outputFolder)
        self.createWaitingTimePlot(outputFolder)
        self.createFuelConsumptionPlot(outputFolder)
        self.createCombinedGraph(outputFolder)

    def createSpeedPlot(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("Speed")
        plt.xlabel("Simulation Time")
        plt.ylabel("avg Speed [m/s]")
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [self.dataPoints[i]["speed"] for i in range(self.maxSimSteps)],
                self.aggrGroups,
            ),
        )
        plt.savefig(os.path.join(outputFolder, f"speed.png"), dpi=self.dpi)
        plt.close()

    def createOccupancyPlot(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("Occupancy")
        plt.xlabel("Simulation Time")
        plt.ylabel("Occupancy")
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [self.dataPoints[i]["occupancy"] for i in range(self.maxSimSteps)],
                self.aggrGroups,
            ),
        )
        plt.savefig(os.path.join(outputFolder, f"occupancy.png"), dpi=self.dpi)
        plt.close()

    def createEmissionsPlot(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("Emissions")
        plt.xlabel("Simulation Time")
        plt.ylabel("Emissions [mg]")
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [self.dataPoints[i]["emissions"] for i in range(self.maxSimSteps)],
                self.aggrGroups,
            ),
        )
        plt.savefig(os.path.join(outputFolder, f"emissions.png"), dpi=self.dpi)
        plt.close()

    def createTraveltimePlot(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("Traveltime")
        plt.xlabel("Simulation Time")
        plt.ylabel("Traveltime")
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [self.dataPoints[i]["traveltime"] for i in range(self.maxSimSteps)],
                self.aggrGroups,
            ),
        )
        plt.savefig(
            os.path.join(outputFolder, f"traveltime.png"),
            dpi=self.dpi,
        )
        plt.close()

    def createVehicleNumberPlot(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("VehicleNumber")
        plt.xlabel("Simulation Time")
        plt.ylabel("number of vehicles")
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [
                    self.dataPoints[i]["lastStepVehicleNumber"]
                    for i in range(self.maxSimSteps)
                ],
                self.aggrGroups,
            ),
        )
        plt.savefig(
            os.path.join(outputFolder, f"vehicleNumber.png"),
            dpi=self.dpi,
        )
        plt.close()

    def createHaltingNumberPlot(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("HaltingNumber")
        plt.xlabel("Simulation Time")
        plt.ylabel("number of halting vehicles (speed < 0.1 [m/s]")
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [
                    self.dataPoints[i]["lastStepHaltingNumber"]
                    for i in range(self.maxSimSteps)
                ],
                self.aggrGroups,
            ),
        )
        plt.savefig(
            os.path.join(outputFolder, f"haltingNumber.png"),
            dpi=self.dpi,
        )
        plt.close()

    def createNoisePlot(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("Noise")
        plt.xlabel("Simulation Time")
        plt.ylabel("Noise [db]")
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [self.dataPoints[i]["Noise"] for i in range(self.maxSimSteps)],
                self.aggrGroups,
            ),
        )
        plt.savefig(os.path.join(outputFolder, f"noise.png"), dpi=self.dpi)
        plt.close()

    def createWaitingTimePlot(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("WaitingTime")
        plt.xlabel("Simulation Time")
        plt.ylabel("sum of vehicle waiting time")
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [self.dataPoints[i]["WaitingTime"] for i in range(self.maxSimSteps)],
                self.aggrGroups,
            ),
        )
        plt.savefig(
            os.path.join(outputFolder, f"waitingTime.png"),
            dpi=self.dpi,
        )
        plt.close()

    def createFuelConsumptionPlot(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("FuelConsumption")
        plt.xlabel("Simulation Time")
        plt.ylabel("FuelConsumption [ml]")
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [
                    self.dataPoints[i]["FuelConsumption"]
                    for i in range(self.maxSimSteps)
                ],
                self.aggrGroups,
            ),
        )
        plt.savefig(
            os.path.join(outputFolder, f"fuelConsumption.png"),
            dpi=600,
        )
        plt.close()

    def createCombinedGraph(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("Overview")
        plt.xlabel("Simulation Time")
        plt.ylabel("Overview")
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [self.dataPoints[i]["speed"] for i in range(self.maxSimSteps)],
                self.aggrGroups,
            ),
            label="Speed [m/s]",
        )
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [
                    self.dataPoints[i]["emissions"] * 0.001
                    for i in range(self.maxSimSteps)
                ],
                self.aggrGroups,
            ),
            label="Emissions [kg]",
        )
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [self.dataPoints[i]["Noise"] for i in range(self.maxSimSteps)],
                self.aggrGroups,
            ),
            label="Noise [db]",
        )
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [
                    self.dataPoints[i]["lastStepVehicleNumber"]
                    for i in range(self.maxSimSteps)
                ],
                self.aggrGroups,
            ),
            label="VehicleNumber",
        )
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [
                    self.dataPoints[i]["lastStepHaltingNumber"]
                    for i in range(self.maxSimSteps)
                ],
                self.aggrGroups,
            ),
            label="HaltingNumber",
        )
        plt.legend(
            loc="upper center",
            bbox_to_anchor=(0.5, 1.05),
            ncol=3,
            fancybox=True,
            shadow=True,
        )
        plt.savefig(os.path.join(outputFolder, f"combined.png"), dpi=self.dpi)
        plt.close()


class EdgeStatsCollector:
    def __init__(self, maxSimSteps, diagOut, jsonOut, simId=""):
        self.maxSimSteps = maxSimSteps
        self.edgeStats = {}
        self.simId = simId
        self.diagOut = f"{diagOut}/{simId}"
        self.jsonOut = f"{jsonOut}/{simId}"

    def registerEdge(self, edgeId):
        self.edgeStats[edgeId] = EdgeStats(edgeId, self.maxSimSteps, self.simId)

    def registerAllRelevantEdges(self):
        allEdges = traci.edge.getIDList()
        for edgeId in allEdges:
            #if edgeId.startswith("e") and "_t" not in edgeId:
            self.registerEdge(edgeId)

    def collect(self, simStep):
        for edgeId in self.edgeStats:
            self.edgeStats[edgeId].createDatapoint(simStep)

    def getEdgeStats(self):
        return self.edgeStats

    def getEdgeStatsAsJson(self):
        return json.dumps(self.edgeStats)

    def createDiags(self):
        self.__ensureFolder(self.diagOut)
        for edgeId in self.edgeStats:
            self.__ensureFolder(self.diagOut + "/" + edgeId)
            edgeStats = self.edgeStats[edgeId]
            edgeStats.createPlots(self.diagOut + "/" + edgeId)

    def writeJSON(self):
        self.__ensureFolder(self.jsonOut)
        for edgeId in self.edgeStats:
            edgeStats = self.edgeStats[edgeId]
            edgeStats.writeJson(self.jsonOut)

    def sendJsonToSplunk(self, dest, token):
        logging.info("Sending JSON to Splunk")
        with requests.Session() as s:
            for edgeId, edgeStat in self.edgeStats.items():
                url = "https://{}/services/collector/event".format(dest)
                authHeader = {"Authorization": "Splunk {}".format(token)}
                jsonDict = {"index": "hack", "event": edgeStat.serialize()}

                r = s.post(url, headers=authHeader, json=jsonDict, verify=False)
                if r.status_code != 200:
                    logging.error(
                        "Failed to send json to splunk. Status code: {}".format(
                            r.status_code
                        )
                    )
                else:
                    logging.debug(
                        "Successfully sent json to splunk for edge {}".format(edgeId)
                    )

    def sendXMLToSplunk(self, dest, token, xmlFilePath):
        logging.info("Sending XML to Splunk (but it's actually JSON, don't worry)")
        with requests.Session() as s:
            url = "https://{}/services/collector/event".format(dest)
            authHeader = {"Authorization": "Splunk {}".format(token)}
            jsonDict = {"index": "hack", "event": getJSONFromXML(xmlFilePath)}
            r = s.post(
                url,
                headers=authHeader,
                json=jsonDict,
                verify=False,
            )
            if r.status_code != 200:
                logging.error(
                    "Failed to send xml to splunk. Status code: {}".format(
                        r.status_code
                    )
                )
            else:
                logging.debug("Successfully sent xml to splunk")

    def __ensureFolder(self, path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
