First, you have to install the sumo modules:

```
pip install sumolib
pip install traci
```

To generate a net from edges and nodes and what not... , run:

```
netconvert --node-files=nets/lucerne.nod.xml --edge-files=nets/lucerne.edg.xml --output-file=nets/lucerne.net.xml
duarouter -n nets/lucerne.net.xml --route-files nets/lucerne.trips.xml -o nets/lucerne.rou.xml --ignore-errors
python3 tools/vehicleTypeChanger.py
```

To set the vehicle types, run the following command:

``` 
python3 tools/vehicleTypeChanger.py
```

To generate a not to random trip selection, configure the exmpleTrips.yaml file in tools and the script. Paste the output into the trips file and run duarouter:
```
python3 tools/generateTrips.py
``` 

run with:

```
sumo -c config/hello.sumocfg
```

or

```
sumo-gui -c config/hello.sumocfg
```

or run simulation with

```
python main.py
```