from time import sleep
import sumolib
import traci

import src.util as util
import src.tlsControl as tlsControl

SIM_STEPS = 500
WITH_GUI = True
VIEW_ID = "View #0"
ZOOM_LVL = 2000
#CENTER_X, CENTER_Y = 4577.56, 4533.25
CENTER_X, CENTER_Y = 4912.04, 3512.10

if WITH_GUI:
    sumoBinary = sumolib.checkBinary("sumo-gui")
else:
    sumoBinary = sumolib.checkBinary("sumo")

cmd = [sumoBinary, "-c", "naefels-2/osm.sumocfg"]

traci.start(cmd)

if WITH_GUI:
    traci.gui.setZoom(VIEW_ID, ZOOM_LVL)
    traci.gui.setOffset(VIEW_ID, CENTER_X, CENTER_Y)


id_list = [
    "31379675",
    "664067024",
    "664067031",
    "8496857761",
    "cluster_1717556357_30044884",
    "cluster_1717556395_31379676",
    "cluster_30044888_5438046964_8582794941_8582794942",
    "cluster_8582788745_8582788746",
]

tls_states = {
    "31379675": "gggrrrggg",  # Näfels, SGU; Reihenfolge: EEE, SSS, NNN
    "664067024": "rr",  # Zwischen Näfels und Netstal, 80er Strecke
    "664067031": "rr",  # Oberurnen bahnübergang
    "8496857761": "rrrrrrrr",  # part of Bahnhof Näfels
    "cluster_1717556357_30044884": "rr",  # part of Bahnhof Näfels
    "cluster_1717556395_31379676": "rr",  # Nördlich vom Bahnhof Näfels, Gentile
    "cluster_30044888_5438046964_8582794941_8582794942": "rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr",  # part of Bahnhof Näfels
    "cluster_8582788745_8582788746": "ggggggggg",  # unbekannt :(
}

TLS_ID = "8496857761"
sguTls = tlsControl.TLSControl(TLS_ID, "111222333", "rrrrrrrrr")
# sguTls.print_state()
# print("setting first light, second and third to green")
# sguTls.set("1", 1, "g")
# sguTls.set("1", 2, "g")
# sguTls.print_state()
# print("setting 3rd light, 0 and 1 to G")
# sguTls.set("3", 0, "G")
# sguTls.set("3", 1, "G")
# sguTls.print_state()

vehs_at_tls = []

step = 0
while step < SIM_STEPS:
    traci.simulationStep()
    # print TLS state & sleep for 100ms
    # print("Step: {}".format(step))
    # print("TLS state: {}".format(traci.trafficlight.getRedYellowGreenState(TLS_ID)))
    # print("\n")
    # sguTls.set_state(traci.trafficlight.getRedYellowGreenState(TLS_ID))
    # sguTls.print_state()
    # sleep(0.1)

    curr_vehs = util.get_all_vehs_at_tls(TLS_ID)
    for veh in curr_vehs:
        if veh not in vehs_at_tls:
            vehs_at_tls.append(veh)

    step += 1

veh_stats = util.get_veh_stats(vehs_at_tls)
avg_veh_stats = util.get_avg_veh_stats(veh_stats)

# print vehicle statistics
print(f"Vehicle statistics for {len(vehs_at_tls)} vehicles :")
print("\n".join(["{}: {}".format(key, value) for key, value in avg_veh_stats.items()]))

traci.close()
