"""
__author__ = "Paul Waldecker"
__email__ = "0157@htl.rennweg.at"
__version__ = "0.1"
__copyright__ = "Copyright 2024"
__license__ = "GPL"
__status__ = "In Progress"
"""


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


def main():
    # A.1 -------------------------------------

    # A.1.1 -------------
    print(fermat(2))
    print(fermat(3))
    print(fermat(5))
    print(fermat(7))
    print(fermat(997))


if __name__ == "__main__":
    main()
