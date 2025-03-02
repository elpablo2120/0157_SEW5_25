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
    """
    Liest ein CSV-File ein und gibt eine Liste von Tupeln zurück
    :param file_path: Pfad zur CSV-Datei
    :return: Liste von Tupeln mit (timestamp, lon, lat, altitude)
    """
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
    """
    Liest ein GPX-File ein und gibt eine Liste von Tupeln zurück
    :param file_path: Pfad zur GPX-Datei
    :return: Liste von Tupeln mit (timestamp, lon, lat, altitude)
    """
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
    """
    Filtert die Daten nach Seehöhe
    :param data: Liste von Tupeln mit (timestamp, lon, lat, altitude)
    :param min_alt: Minimale Seehöhe
    :param max_alt: Maximale Seehöhe
    :return: Gefilterte Liste von Tupeln mit (timestamp, lon, lat, altitude)
    """
    filtered_data = []
    for point in data:
        altitude = point[3]
        if (min_alt is None or altitude >= min_alt) and (max_alt is None or altitude <= max_alt):
            filtered_data.append(point)
    return filtered_data

def plot_data(data: List[Tuple], args: argparse.Namespace) -> None:
    """
    Erstellt ein Scatterplot der Daten
    :param data: Liste von Tupeln mit (timestamp, lon, lat, altitude)
    :param args: Argumente des Programms
    """
    x = [point[1] for point in data]
    y = [point[2] for point in data]
    colors = tuple([int(c) / 255 for c in args.dot.split(',')]) if args.dot else (0, 0, 1)
    line_color = tuple([int(c) / 255 for c in args.line.split(',')]) if args.line else (0, 1, 0)

    plt.scatter(x, y, color=[colors], alpha=0.5)
    if args.connect:
        plt.plot(x, y, color=line_color, alpha=0.5)
    if args.marker:
        plt.scatter([x[0], x[-1]], [y[0], y[-1]], color="red", marker="x")
        plt.annotate('Start', xy=(x[0], y[0]), xytext=(x[0] - 0.005, y[0] + 0.005),
                     arrowprops=dict(facecolor='blue', shrink=0.05))
        plt.annotate('End', xy=(x[-1], y[-1]), xytext=(x[-1] + 0.005, y[-1] - 0.005),
                     arrowprops=dict(facecolor='red', shrink=0.05))

    plt.savefig(args.out)

def save_csv(data, file_path):
    """
    Speichert die Daten in einer CSV-Datei
    :param data: Liste von Tupeln mit (timestamp, lon, lat, altitude)
    :param file_path: Pfad zur CSV-Datei
    """
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for row in data:
            writer.writerow(row)


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

    # Datei basierend auf dem Dateityp laden
    data = read_csv(args.infile) if args.infile.endswith(".csv") else read_gpx(args.infile)
    data = filter_by_altitude(data, args.tal, args.spitze)

    # Ausgabe für verbose
    if args.verbose and not args.quiet:
        altitudes = [point[3] for point in data]
        print(f"Niedrigster Punkt: {min(altitudes)}")
        print(f"Höchster Punkt: {max(altitudes)}")
        print(f"Anzahl der Wegpunkte: {len(data)}")
        if args.marker:
            print(f"Startpunkt: {data[0]}")
            print(f"Endpunkt: {data[-1]}")

    # Ausgabe basierend auf Dateityp
    if args.out.endswith(".csv"):
        save_csv(data, args.out)
    elif args.out.endswith(".png"):
        plot_data(data, args)
    else:
        print("Invalid output file extension. Only .csv or .png are allowed.")

if __name__ == "__main__":
    main()