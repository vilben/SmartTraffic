import random
import xml.etree.ElementTree as ET


INPUT = "../nets/lucerne.rou.xml"
OUTPUT = "../nets/lucerne.rou.xml"

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
    pass


if __name__ == "__main__":
    main()
