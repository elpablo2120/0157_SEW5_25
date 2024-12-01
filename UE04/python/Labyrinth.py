
#suchen
#alleSuchen
#getLabyrinthFromFile

def fromStrings(map: list[str]) -> list[list[str]]:
    return [list(x) for x in map]

def printLabyrinth(lab: list[list[str]]) -> None:
    for row in lab:
        print("".join(row))

def suchen(zeile: int, spalte: int, lab: list[list[int]]) -> bool:
    if lab[zeile][spalte] == 'A':
        return True

    if lab[zeile][spalte] == '#' or lab[zeile][spalte] == '.':
        return False

    lab[zeile][spalte] = '.'

    found = (suchen(zeile-1, spalte, lab) or
                 suchen(zeile+1, spalte, lab) or
                 suchen(zeile, spalte-1, lab) or
                 suchen(zeile, spalte+1, lab))

    lab[zeile][spalte] = ' '

    return found

def alleSuchen

if 'name' == '__main__':
