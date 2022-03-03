pip install sumolib

To convert edges and nodes to a net, run:

```
netconvert --node-files=hello.nod.xml --edge-files=hello.edg.xml --output-file=hello.net.xml
```

run with:

```
sumo -c config/hello.sumocfg
```

or

```
sumo-gui -c config/hello.sumocfg
```