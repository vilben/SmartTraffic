import sumolib
import traci

sumoBinary = sumolib.checkBinary("sumo-gui")

cmd = [sumoBinary, "-c", "config/lucerne.sumo.cfg"]

traci.start(cmd)

step = 0
while step < 1000:
    traci.simulationStep()
    # whatever... tutorial stuff
    # if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
    #     traci.trafficlight.setRedYellowGreenState("0", "GrGr")
    step += 1

traci.close()

