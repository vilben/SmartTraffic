import errno
import json
import os
import traci
from matplotlib import pyplot as plt


class EdgeStats:
    def __init__(self, edgeId, maxSimSteps):
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
            "lastStepVehicleIDs": traci.edge.getLastStepVehicleIDs(self.edgeId),
            "Noise": traci.edge.getNoiseEmission(self.edgeId),
            "WaitingTime": traci.edge.getWaitingTime(self.edgeId),
            "FuelConsumption": traci.edge.getFuelConsumption(self.edgeId),
        }

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
        plt.figure(figsize=(20, 10))
        plt.title("Speed")
        plt.xlabel("SimStep")
        plt.ylabel("avg Speed [m/s]")
        plt.plot(
            range(self.maxSimSteps),
            [self.dataPoints[i]["speed"] for i in range(self.maxSimSteps)],
        )
        plt.savefig(os.path.join(outputFolder, "speed.png"), dpi=600)
        plt.close()

    def createOccupancyPlot(self, outputFolder):
        plt.figure(figsize=(20, 10))
        plt.title("Occupancy")
        plt.xlabel("SimStep")
        plt.ylabel("Occupancy")
        plt.plot(
            range(self.maxSimSteps),
            [self.dataPoints[i]["occupancy"] for i in range(self.maxSimSteps)],
        )
        plt.savefig(os.path.join(outputFolder, "occupancy.png"), dpi=600)
        plt.close()

    def createEmissionsPlot(self, outputFolder):
        plt.figure(figsize=(20, 10))
        plt.title("Emissions")
        plt.xlabel("SimStep")
        plt.ylabel("Emissions [mg]")
        plt.plot(
            range(self.maxSimSteps),
            [self.dataPoints[i]["emissions"] for i in range(self.maxSimSteps)],
        )
        plt.savefig(os.path.join(outputFolder, "emissions.png"), dpi=600)
        plt.close()

    def createTraveltimePlot(self, outputFolder):
        plt.figure(figsize=(20, 10))
        plt.title("Traveltime")
        plt.xlabel("SimStep")
        plt.ylabel("Traveltime")
        plt.plot(
            range(self.maxSimSteps),
            [self.dataPoints[i]["traveltime"] for i in range(self.maxSimSteps)],
        )
        plt.savefig(os.path.join(outputFolder, "traveltime.png"), dpi=600)
        plt.close()

    def createVehicleNumberPlot(self, outputFolder):
        plt.figure(figsize=(20, 10))
        plt.title("VehicleNumber")
        plt.xlabel("SimStep")
        plt.ylabel("number of vehicles")
        plt.plot(
            range(self.maxSimSteps),
            [
                self.dataPoints[i]["lastStepVehicleNumber"]
                for i in range(self.maxSimSteps)
            ],
        )
        plt.savefig(os.path.join(outputFolder, "vehicleNumber.png"), dpi=600)
        plt.close()

    def createHaltingNumberPlot(self, outputFolder):
        plt.figure(figsize=(20, 10))
        plt.title("HaltingNumber")
        plt.xlabel("SimStep")
        plt.ylabel("number of halting vehicles (speed < 0.1 [m/s]")
        plt.plot(
            range(self.maxSimSteps),
            [
                self.dataPoints[i]["lastStepHaltingNumber"]
                for i in range(self.maxSimSteps)
            ],
        )
        plt.savefig(os.path.join(outputFolder, "haltingNumber.png"), dpi=600)
        plt.close()

    def createNoisePlot(self, outputFolder):
        plt.figure(figsize=(20, 10))
        plt.title("Noise")
        plt.xlabel("SimStep")
        plt.ylabel("Noise [db]")
        plt.plot(
            range(self.maxSimSteps),
            [self.dataPoints[i]["Noise"] for i in range(self.maxSimSteps)],
        )
        plt.savefig(os.path.join(outputFolder, "noise.png"), dpi=600)
        plt.close()

    def createWaitingTimePlot(self, outputFolder):
        plt.figure(figsize=(20, 10))
        plt.title("WaitingTime")
        plt.xlabel("SimStep")
        plt.ylabel("sum of vehicle waiting time")
        plt.plot(
            range(self.maxSimSteps),
            [self.dataPoints[i]["WaitingTime"] for i in range(self.maxSimSteps)],
        )
        plt.savefig(os.path.join(outputFolder, "waitingTime.png"), dpi=600)
        plt.close()

    def createFuelConsumptionPlot(self, outputFolder):
        plt.figure(figsize=(20, 10))
        plt.title("FuelConsumption")
        plt.xlabel("SimStep")
        plt.ylabel("FuelConsumption [ml]")
        plt.plot(
            range(self.maxSimSteps),
            [self.dataPoints[i]["FuelConsumption"] for i in range(self.maxSimSteps)],
        )
        plt.savefig(os.path.join(outputFolder, "fuelConsumption.png"), dpi=600)
        plt.close()

    def createCombinedGraph(self, outputFolder):
        plt.figure(figsize=(20, 10))
        plt.title("Overview")
        plt.xlabel("SimStep")
        plt.ylabel("Overview")
        plt.plot(
            range(self.maxSimSteps),
            [self.dataPoints[i]["speed"] for i in range(self.maxSimSteps)],
            label="Speed [m/s]",
        )
        plt.plot(
            range(self.maxSimSteps),
            [self.dataPoints[i]["emissions"] * 0.001 for i in range(self.maxSimSteps)],
            label="Emissions [kg]",
        )
        plt.plot(
            range(self.maxSimSteps),
            [self.dataPoints[i]["Noise"] for i in range(self.maxSimSteps)],
            label="Noise [db]",
        )
        plt.plot(
            range(self.maxSimSteps),
            [
                self.dataPoints[i]["lastStepVehicleNumber"]
                for i in range(self.maxSimSteps)
            ],
            label="VehicleNumber",
        )
        plt.plot(
            range(self.maxSimSteps),
            [
                self.dataPoints[i]["lastStepHaltingNumber"]
                for i in range(self.maxSimSteps)
            ],
            label="HaltingNumber",
        )
        plt.legend(
            loc="upper center",
            bbox_to_anchor=(0.5, 1.05),
            ncol=3,
            fancybox=True,
            shadow=True,
        )
        plt.savefig(os.path.join(outputFolder, "combined.png"), dpi=600)
        plt.close()


class EdgeStatsCollector:
    def __init__(self, maxSimSteps):
        self.maxSimSteps = maxSimSteps
        self.edgeStats = {}

    def registerEdge(self, edgeId):
        self.edgeStats[edgeId] = EdgeStats(edgeId, self.maxSimSteps)

    def collect(self, simStep):
        for edgeId in self.edgeStats:
            self.edgeStats[edgeId].createDatapoint(simStep)

    def getEdgeStats(self):
        return self.edgeStats

    def getEdgeStatsAsJson(self):
        return json.dumps(self.edgeStats)

    def createDiags(self, outFolder):
        self.__ensureFolder(outFolder)
        for edgeId in self.edgeStats:
            self.__ensureFolder(outFolder + "/" + edgeId)
            edgeStats = self.edgeStats[edgeId]
            edgeStats.createPlots(outFolder + "/" + edgeId)

    def __ensureFolder(self, path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
