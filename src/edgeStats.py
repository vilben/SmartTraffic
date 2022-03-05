import errno
import json
import os
import requests
import traci
from matplotlib import pyplot as plt

from src.diagUtil import aggregateSeries


class EdgeStats:
    def __init__(self, edgeId, maxSimSteps, namePrefix):
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
        self.namePrefix = namePrefix
        self.figSize = (20, 10)
        self.dpi = 300

    def createDatapoint(self, simStep):
        self.dataPoints[simStep] = {
            "edgeId": self.edgeId,
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
        with open(os.path.join(outputFolder, f"{self.namePrefix}_data.json"), "w") as f:
            json.dump(self.dataPoints, f)

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
        plt.xlabel("SimStep")
        plt.ylabel("avg Speed [m/s]")
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [self.dataPoints[i]["speed"] for i in range(self.maxSimSteps)],
                self.aggrGroups,
            ),
        )
        plt.savefig(
            os.path.join(outputFolder, f"{self.namePrefix}_speed.png"), dpi=self.dpi
        )
        plt.close()

    def createOccupancyPlot(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("Occupancy")
        plt.xlabel("SimStep")
        plt.ylabel("Occupancy")
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [self.dataPoints[i]["occupancy"] for i in range(self.maxSimSteps)],
                self.aggrGroups,
            ),
        )
        plt.savefig(
            os.path.join(outputFolder, f"{self.namePrefix}_occupancy.png"), dpi=self.dpi
        )
        plt.close()

    def createEmissionsPlot(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("Emissions")
        plt.xlabel("SimStep")
        plt.ylabel("Emissions [mg]")
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [self.dataPoints[i]["emissions"] for i in range(self.maxSimSteps)],
                self.aggrGroups,
            ),
        )
        plt.savefig(
            os.path.join(outputFolder, f"{self.namePrefix}_emissions.png"), dpi=self.dpi
        )
        plt.close()

    def createTraveltimePlot(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("Traveltime")
        plt.xlabel("SimStep")
        plt.ylabel("Traveltime")
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [self.dataPoints[i]["traveltime"] for i in range(self.maxSimSteps)],
                self.aggrGroups,
            ),
        )
        plt.savefig(
            os.path.join(outputFolder, f"{self.namePrefix}_traveltime.png"),
            dpi=self.dpi,
        )
        plt.close()

    def createVehicleNumberPlot(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("VehicleNumber")
        plt.xlabel("SimStep")
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
            os.path.join(outputFolder, f"{self.namePrefix}_vehicleNumber.png"),
            dpi=self.dpi,
        )
        plt.close()

    def createHaltingNumberPlot(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("HaltingNumber")
        plt.xlabel("SimStep")
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
            os.path.join(outputFolder, f"{self.namePrefix}_haltingNumber.png"),
            dpi=self.dpi,
        )
        plt.close()

    def createNoisePlot(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("Noise")
        plt.xlabel("SimStep")
        plt.ylabel("Noise [db]")
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [self.dataPoints[i]["Noise"] for i in range(self.maxSimSteps)],
                self.aggrGroups,
            ),
        )
        plt.savefig(
            os.path.join(outputFolder, f"{self.namePrefix}_noise.png"), dpi=self.dpi
        )
        plt.close()

    def createWaitingTimePlot(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("WaitingTime")
        plt.xlabel("SimStep")
        plt.ylabel("sum of vehicle waiting time")
        plt.plot(
            range(self.seriesLength),
            aggregateSeries(
                [self.dataPoints[i]["WaitingTime"] for i in range(self.maxSimSteps)],
                self.aggrGroups,
            ),
        )
        plt.savefig(
            os.path.join(outputFolder, f"{self.namePrefix}_waitingTime.png"),
            dpi=self.dpi,
        )
        plt.close()

    def createFuelConsumptionPlot(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("FuelConsumption")
        plt.xlabel("SimStep")
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
            os.path.join(outputFolder, f"{self.namePrefix}_fuelConsumption.png"),
            dpi=600,
        )
        plt.close()

    def createCombinedGraph(self, outputFolder):
        plt.figure(figsize=self.figSize)
        plt.title("Overview")
        plt.xlabel("SimStep")
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
        plt.savefig(
            os.path.join(outputFolder, f"{self.namePrefix}_combined.png"), dpi=self.dpi
        )
        plt.close()


class EdgeStatsCollector:
    def __init__(self, maxSimSteps, namePrefix=""):
        self.maxSimSteps = maxSimSteps
        self.edgeStats = {}
        self.namePrefix = namePrefix

    def registerEdge(self, edgeId):
        self.edgeStats[edgeId] = EdgeStats(edgeId, self.maxSimSteps, self.namePrefix)

    def collect(self, simStep):
        for edgeId in self.edgeStats:
            self.edgeStats[edgeId].createDatapoint(simStep)

    def getEdgeStats(self):
        return self.edgeStats

    def getEdgeStatsAsJson(self):
        return json.dumps(self.edgeStats)

    def sendJsonToSplunk(self):

        with requests.Session() as s:
            for edgeStat in self.edgeStats:
                url='https://192.168.1.190:8088/services/collector/event'
                authHeader = {'Authorization': 'Splunk {}'.format('367a51f8-0ffd-4b88-884a-4dbbdf5ebc4a')}
                jsonDict = {"index":"hack", "event": { 'message' : json.dumps(edgeStat)} }

                print(authHeader)
                print(jsonDict)

                r = s.post(url, headers=authHeader, json=jsonDict, verify=False)

    def createDiags(self, outFolder):
        self.__ensureFolder(outFolder)
        for edgeId in self.edgeStats:
            self.__ensureFolder(outFolder + "/" + edgeId)
            edgeStats = self.edgeStats[edgeId]
            edgeStats.createPlots(outFolder + "/" + edgeId)
            edgeStats.writeJson(outFolder + "/" + edgeId)

    def __ensureFolder(self, path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
