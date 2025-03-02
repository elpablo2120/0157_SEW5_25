from argparse import ArgumentParser
import time

def fromStrings(map: list[str]) -> list[list[str]]:
    """
    Konvertiert eine Liste von Strings in eine Liste von Listen
    @param map: Die Liste von Strings
    @return: Die Liste von Listen
    """
    return [list(x) for x in map]

def printLabyrinth(lab: list[list[str]]) -> None:
    """
    Gibt das Labyrinth auf der Konsole aus
    @param lab: Das Labyrinth als Liste von Listen
    @return: None
    """
    for row in lab:
        print("".join(row))

def suchen(zeile: int, spalte: int, lab: list[list[str]]) -> bool:
    """
    Sucht den Ausgang im Labyrinth
    @param zeile: Die Zeile, von der aus gesucht wird
    @param spalte: Die Spalte, von der aus gesucht wird
    @param lab: Das Labyrinth als Liste von Listen
    @return: True, wenn der Ausgang gefunden wurde, sonst False
    """
    if lab[zeile][spalte] == 'A':
        return True
    if lab[zeile][spalte] in ('#', '.'):
        return False
    lab[zeile][spalte] = '.'
    found = (suchen(zeile-1, spalte, lab) or
             suchen(zeile+1, spalte, lab) or
             suchen(zeile, spalte-1, lab) or
             suchen(zeile, spalte+1, lab))
    lab[zeile][spalte] = ' '
    return found

def alleSuchen(zeile: int, spalte: int, lab: list[list[str]]) -> int:
    """
    Sucht alle möglichen Wege zum Ausgang im Labyrinth
    @param zeile: Die Zeile, von der aus gesucht wird
    @param spalte: Die Spalte, von der aus gesucht wird
    @param lab: Das Labyrinth als Liste von Listen
    @return: Die Anzahl der Wege zum Ausgang
    """
    if lab[zeile][spalte] == 'A':
        return 1
    if lab[zeile][spalte] in ('#', '.'):
        return 0
    lab[zeile][spalte] = '.'
    anzahl = (alleSuchen(zeile-1, spalte, lab) +
              alleSuchen(zeile+1, spalte, lab) +
              alleSuchen(zeile, spalte-1, lab) +
              alleSuchen(zeile, spalte+1, lab))
    lab[zeile][spalte] = ' '  # Reset the cell to its original state
    return anzahl

def main():
    # Delay fehlt
    parser = ArgumentParser(description="Calculate number of ways through a labyrinth - Paul Waldecker 5CN")
    parser.add_argument("filename", help="File containing the labyrinth to solve")
    parser.add_argument("-x", "--xstart", metavar="XSTART", type=int, help="X-coordinate to start", default=1)
    parser.add_argument("-y", "--ystart", metavar="YSTART", type=int, help="Y-coordinate to start", default=1)
    parser.add_argument("-p", "--print", action="store_true", help="Print output of every solution")
    parser.add_argument("-t", "--time", action="store_true", help="Print total calculation time (in milliseconds)")
    parser.add_argument("-d", "--delay", metavar="DELAY", type=int, help="Delay after printing a solution (in milliseconds)", default=500)
    args = parser.parse_args()

    with open(args.filename) as f:
        lab = fromStrings(f.read().splitlines())

    if args.print:
        print("Initial Labyrinth:")
        printLabyrinth(lab)
        print()

    start_zeile, start_spalte = args.ystart, args.xstart

    if args.time:
        start_time = time.time()

    if suchen(start_zeile, start_spalte, lab):
        print("Ausgang gefunden: Ja")
    else:
        print("Ausgang gefunden: Nein")

    print("Anzahl der Wege zum Ausgang:", alleSuchen(start_zeile, start_spalte, lab))

    if args.time:
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000  # Zeit in Millisekunden
        print(f"Berechnungszeit: {elapsed_time:.2f} ms")

if __name__ == '__main__':
    main()
