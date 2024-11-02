"""
__author__ = "Paul Waldecker"
__email__ = "0157@htl.rennweg.at"
__version__ = "3.0"
__copyright__ = "Copyright 2024"
__license__ = "GPL"
__status__ = "Ready to Review"
"""
import argparse
import csv
from typing import List, Tuple
import xml.etree.ElementTree as ET

from matplotlib import pyplot as plt


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

def filter_by_altitude(data: List[Tuple], min_alt: float, max_alt: float) -> List[Tuple]:
    filtered_data = []
    for point in data:
        altitude = point[3]
        if (min_alt is None or altitude >= min_alt) and (max_alt is None or altitude <= max_alt):
            filtered_data.append(point)
    return filtered_data

def plot_data(data: List[Tuple], args: argparse.Namespace) -> None:
    x = [point[1] for point in data]
    y = [point[2] for point in data]
    colors = tuple([int(c) / 255 for c in args.dot.split(',')]) if args.dot else (0, 0, 1)
    line_color = tuple([int(c) / 255 for c in args.line.split(',')]) if args.line else (0, 1, 0)

    plt.scatter(x, y, color=[colors], alpha=0.5)
    if args.connect:
        plt.plot(x, y, color=line_color, alpha=0.5)
    if args.marker:
        plt.scatter([x[0], x[-1]], [y[0], y[-1]], color="red", marker="x")

    plt.savefig(args.out)


def main():
    parser = argparse.ArgumentParser(description="skitrack by Paul Waldecker")
    parser.add_argument("infile", help="Input-Datei (z.B. track.gpx oder track.csv)")
    parser.add_argument("-o", "--out", help="Zu generierende Datei, z.B. ski.csv oder ski.png")
    parser.add_argument("-m", "--marker", action="store_true", help="Sollen der erste und letzte Punkt markiert werden?")
    parser.add_argument("-t", "--tal", type=float, help="Seehöhe des niedrigsten Punktes, der noch ausgewertet werden soll")
    parser.add_argument("-s", "--spitze", type=float, help="Seehöhe des höchsten Punktes, der noch ausgewertet werden soll")
    parser.add_argument("-d", "--dot", help="RGB color for points, e.g., 128,128,255")
    parser.add_argument("-c", "--connect", action="store_true", help="Connect points with lines")
    parser.add_argument("-l", "--line", help="RGB-Farbe der Linien z.B.: 255,128,255")
    parser.add_argument("-v", "--verbose", action="store_true", help="Zeigt Details an")
    parser.add_argument("-q", "--quiet", action="store_true", help="keine Textausgabe")
    args = parser.parse_args()

    data = read_csv(args.infile) if args.infile.endswith(".csv") else read_gpx(args.infile)


if __name__ == "__main__":
    #print(read_csv("ski.csv"))
    #print(read_gpx("ski.gpx"))
    main()