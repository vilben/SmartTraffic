import sumolib
import traci

sumoBinary = sumolib.checkBinary("sumo-gui")

cmd = [sumoBinary, "-c", "config/hello.sumocfg"]

traci.start(cmd)
