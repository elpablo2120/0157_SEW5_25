
#suchen
#alleSuchen
#getLabyrinthFromFile

def fromStrings(map: list[str]) -> list[list[str]]:
    return [list(x) for x in map]

def printLabyrinth(lab: list[list[str]]) -> None:
    for row in lab:
        print("".join(row))


