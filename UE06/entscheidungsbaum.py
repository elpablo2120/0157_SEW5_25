"""
__author__ = "Paul Waldecker"
__email__ = "0157@htl.rennweg.at"
__version__ = "0.1"
__copyright__ = "Copyright 2025"
__license__ = "GPL"
__status__ = "In Progress"
"""

import csv
from typing import NamedTuple, Optional, TypeVar, List

class Candidate(NamedTuple):
    anfangsbuchstabe: str
    puenktlich: bool
    htl: bool
    sprache: str
    erfolgreich: Optional[bool] = None  # allow unlabeled data

T = TypeVar('T')  # praktisch: generischer Typ für Inputs

def readfile(filename: str) -> List[T]:
    candidates: List[Candidate] = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            anfangsbuchstabe = row['name'][0]
            puenktlich = row['puenktlich'] == 'ja'
            htl = row['htl'] == 'ja'
            sprache = row['sprache']
            erfolgreich = row['erfolgreich'] == 'ja' if row['erfolgreich'] else None
            candidate = Candidate(anfangsbuchstabe, puenktlich, htl, sprache, erfolgreich)
            candidates.append(candidate)
    return candidates


# Funktion zur Partitionierung der Eingaben basierend auf einem Attribut
def partition_by(inputs: List[T], attribute: str) -> Dict[Any, List[T]]:
    """
    Partitioniere die Eingaben in Listen basierend auf dem angegebenen Attribut (Spaltenname).

    Parameters:
    inputs (List[T]): Die Liste der Eingaben, die partitioniert werden sollen.
    attribute (str): Das Attribut, nach dem partitioniert werden soll.

    Returns:
    Dict[Any, List[T]]: Ein Dictionary, dessen Schlüssel die eindeutigen Werte des Attributs sind
                        und dessen Werte Listen von Eingaben mit diesem Attributswert enthalten.
    """
    partitions: Dict[Any, List[T]] = defaultdict(list)
    for input in inputs:
        key = getattr(input, attribute)  # Hole den Wert des angegebenen Attributs
        partitions[key].append(input)  # Füge die Eingabe der entsprechenden Liste hinzu
    return partitions

if __name__ == "__main__":
    candidates = readfile("candidates.csv")
    print(candidates)