"""
__author__ = "Paul Waldecker"
__email__ = "0157@htl.rennweg.at"
__version__ = "3.0"
__copyright__ = "Copyright 2024"
__license__ = "GPL"
__status__ = "Ready to Review"
"""
import csv
from typing import List, Tuple
import xml.etree.ElementTree as ET


def read_csv(file_path: str) -> List[Tuple]:
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            timestamp = row[0]
            lon = float(row[1])
            lat = float(row[2])
            altitude = float(row[3])
            data.append((timestamp, lon, lat, altitude))
    return data

def read_gpx(file_path: str) -> List[Tuple]:
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = []
    for trkpt in root.findall(".//{*}trkpt"):
        lon = float(trkpt.get("lon"))
        lat = float(trkpt.get("lat"))
        altitude = float(trkpt.find("{*}ele").text)
        timestamp = trkpt.find("{*}time").text
        data.append((timestamp, lon, lat, altitude))
    return data




if __name__ == "__main__":
    #print(read_csv("ski.csv"))
    print(read_gpx("ski.gpx"))