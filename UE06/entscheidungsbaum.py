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

def readfile(filename: str) -> List[Candidate]:
    """
    Liest die Kandidaten aus einer CSV-Datei ein und gibt eine Liste von Candidate-Instanzen zurück.

    >>> readfile("candidates.csv")[-1]
    Candidate(anfangsbuchstabe='W', puenktlich=True, htl=True, sprache='Python', erfolgreich=True)
    """
    candidates = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            anfangsbuchstabe = row['name'][0]
            puenktlich = row['puenktlich'].lower() == 'ja'
            htl = row['htl'].lower() == 'ja'
            sprache = row['sprache']
            erfolgreich = None if row['erfolgreich'] == '' else row['erfolgreich'].lower() == 'ja'
            candidate = Candidate(anfangsbuchstabe, puenktlich, htl, sprache, erfolgreich)
            candidates.append(candidate)
    return candidates

if __name__ == "__main__":
    candidates = readfile("candidates.csv")
    print(candidates)