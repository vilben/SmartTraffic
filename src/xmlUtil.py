import xml.etree.ElementTree as ET
import xmltodict


def insertAttrAtTopNode(xmlFilePath, attNamr, attValue):
    """
    Insert an attribute at the top node of an XML file.
    """
    tree = ET.parse(xmlFilePath)
    root = tree.getroot()
    root.set(attNamr, attValue)
    tree.write(xmlFilePath)


def getJSONFromXML(xmlFilePath):
    """
    Get the JSON from an XML file.
    """
    # read raw XML content
    with open(xmlFilePath, "r") as f:
        xml = f.read()
        return xmltodict.parse(xml)
