First, you have to install the sumo modules:

```
pip install sumolib
pip install traci
```

To generate a net from edges and nodes and what not... , run:

```
netconvert --node-files=nets/lucerne.nod.xml --edge-files=nets/lucerne.edg.xml --output-file=nets/lucerne.net.xml
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