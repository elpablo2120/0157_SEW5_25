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

if __name__ == "__main__":
    print(read_csv("ski.csv"))