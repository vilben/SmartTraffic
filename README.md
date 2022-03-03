First, you have to install the sumo modules:

```
pip install sumolib
pip install traci
```

To generate a net from edges and nodes and what not... , run:

```
netconvert --node-files=nets/hello.nod.xml --edge-files=nets/hello.edg.xml --output-file=nets/hello.net.xml
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