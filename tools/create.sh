netconvert --node-files=nets/lucerne.nod.xml --edge-files=nets/lucerne.edg.xml --output-file=nets/lucerne.net.xml --no-turnarounds
duarouter -n nets/lucerne.net.xml --route-files nets/lucerne.trips.xml -o nets/lucerne.rou.xml --ignore-errors
python3 tools/vehicleTypeChanger.py
