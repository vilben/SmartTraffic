import json
import logging
import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import src.xmlUtil


def parseAndEnrichXML(xmlFilePath):
    dict = src.xmlUtil.getJSONFromXML(xmlFilePath)
    simId = dict["emission-export"]["@simId"]
    datapoints = []
    for timestep in dict["emission-export"]["timestep"]:
        for datapoint in timestep["vehicle"]:
            datapoint["time"] = timestep["@time"]
            datapoint["simId"] = simId
            datapoints.append(datapoint)

    return datapoints

def sendAllTheData(events, dest, token):
    logging.info(f"Sending {len(events)} events to {dest}")
    totsent = 0
    with requests.Session() as s:
        for chunk in splitArrayIntoChunks(events, 500000):
            url = "https://{}/services/collector/event".format(dest)
            authHeader = {"Authorization": "Splunk {}".format(token)}
            jsonDict = {"index": "hack", "event": json.dumps(chunk)}

            r = s.post(url, headers=authHeader, json=jsonDict, verify=False)
            totsent = totsent + len(chunk)
            logging.info(
                f"Sent chunk of {len(chunk)} events to {dest} [{totsent}/{len(events)}]"
            )
            if r.status_code != 200:
                logging.error(
                    "Failed to send json to splunk. Status code: {}".format(
                        r.status_code
                    )
                )


def splitArrayIntoChunks(arr, chunkSize):
    return [arr[i : i + chunkSize] for i in range(0, len(arr), chunkSize)]
