"""
__author__ = "Paul Waldecker"
__email__ = "0157@htl.rennweg.at"
__version__ = "1.0"
__copyright__ = "Copyright 2024"
__license__ = "GPL"
__status__ = "Ready to Review"
"""
from collections import Counter


def fermat(p):
    """
    Kleiner Satz von Fermat: a^(p-1) mod p = 1. Bedeutet das wenn p eine Primzahl ist, dann kommt 1 raus. Wenn nicht,
    dann kommt was anderes raus. Dafür muss p eine Primzahl sein.
    :param p: Primzahl bzw Zahl bei der getestet werden soll ob sie eine Primzahl ist
    :return: Liste (mit Länge p-1) von Zahlen, die das Ergebnis der Berechnung a^(p-1) mod p für jede
    Zahl a von 1 bis p-1 sind.
    >>> fermat(2)
    [1]
    >>> fermat(3)
    [1, 1]
    >>> fermat(5)
    [1, 1, 1, 1]
    >>> fermat(7)
    [1, 1, 1, 1, 1, 1]
    >>> fermat(11)
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    """
    return [pow(a, p - 1, p) for a in range(1, p)]


def display(values, p):
    """
    Anzeige der Ergebnisse in Prozent und Anzahl der 1en in der Liste
    :param values: Liste von fermat(p)
    :param p: Primzahl bzw Zahl bei der getestet werden soll ob sie eine Primzahl ist
    :return: Anzahl und Prozent der 1en in der Liste
    >>> display([1, 1, 1, 1, 1, 1], 7)
    7 -> 100.00 % -> res[1]=6, len(res)=6 - [(1, 6)]
    >>> display(fermat(10), 10)
    10 -> 11.11 % -> res[1]=1, len(res)=9 - [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1)]
    """
    counter = Counter(values)
    total = len(values)
    percentage = (counter[1] / total) * 100 if 1 in counter else 0
    print(f"{p} -> {percentage:.2f} % -> res[1]={counter[1]},"
          f" len(res)={total} - {list(counter.items())}")


if __name__ == "__main__":
    primes = list(range(2, 12)) + [997]
    maybe_primes = [9, 15, 21, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562,
                    563, 564, 565, 566, 567, 568, 569, 6601, 8911]

    print("Ergebnisse für Primzahlen von 2 bis 11 und 997:")
    for p in primes:
        display(fermat(p), p)

    print("\nErgebnisse für Nicht-Primzahlen:")
    for p in maybe_primes:
        display(fermat(p), p)
