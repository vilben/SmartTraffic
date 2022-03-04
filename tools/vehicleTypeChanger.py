from operator import add
import random
import xml.etree.ElementTree as ET


INPUT = "nets/lucerne.rou.xml"
OUTPUT = "nets/lucerne.rou.xml"

VEHILCE_TYPES = [
    "normal_car",
    "sporty_car",
    "trailer",
    "coach",
]

VEHICLE_TYPE_WEIGHTS = [
    0.85,
    0.11,
    0.01,
    0.03,
]


def getRandomVehicleType():
    return random.choices(VEHILCE_TYPES, VEHICLE_TYPE_WEIGHTS, k=1)[0]


def parseXml(inputFile):
    tree = ET.parse(inputFile)
    root = tree.getroot()
    return root


def addHardcodedVTypesWithReallyUglyHack():
    XML = """
    <routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">
        <vType id="normal_car" vClass="passenger" maxSpeed="40" speedFactor="0.9" speedDev="0.2" sigma="0.5" color="white" guiShape="passenger" />
        <vType id="sporty_car" vClass="passenger" maxSpeed="60" speedFactor="1.3" speedDev="0.1" sigma="0.1" color="red" guiShape="passenger/sedan" />
        <vType id="trailer" vClass="trailer" maxSpeed="30" speedFactor="1" speedDev="0.05" color="gray" guiShape="truck/trailer" />
        <vType id="coach" vClass="coach" maxSpeed="30" speedFactor="1" speedDev="0.05" color="green" guiShape="bus/coach" />
    """

    # read all lines from INPUT file
    with open(INPUT, "r") as f:
        lines = f.readlines()
        # remove last line
        lines.pop(0)
        lines.insert(0, XML)
        # write all lines to OUTPUT file
        with open(OUTPUT, "w") as f:
            f.writelines(lines)


def main():
    print(f"parsing {INPUT}")
    root = parseXml(INPUT)
    vehicles = root.findall("vehicle")
    print(f"found {len(vehicles)} vehicles")
    for vehicle in vehicles:
        vehicle.set("type", getRandomVehicleType())
    tree = ET.ElementTree(root)
    print(f"writing {OUTPUT}")
    tree.write(OUTPUT)
    if tree.findall("vType") == []:
        addHardcodedVTypesWithReallyUglyHack()


if __name__ == "__main__":
    main()
