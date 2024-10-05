"""
__author__ = "Paul Waldecker"
__email__ = "0157@htl.rennweg.at"
__version__ = "1.0"
__copyright__ = "Copyright 2024"
__license__ = "GPL"
__status__ = "In Progress"
"""
import random

# Globale variable für die ersten 100 Primzahlen
FIRST_100_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                    73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
                    127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
                    179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
                    233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
                    283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
                    353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
                    419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
                    467, 479, 487, 491, 499, 503, 509, 521, 523, 541]


def is_prim_millerrabin(n, k=20):
    """
    Überprüft, ob die gegebene Zahl eine Primzahl ist, indem sie den Miller-Rabin-Test anwendet.

    :param n: Die zu überprüfende Zahl. Sollte größer als 1 sein.
    :param k: Die Anzahl der Durchläufe des Tests. Ein höherer Wert erhöht die Genauigkeit des Tests. Standardwert
                ist 20.
    :return: Gibt "probably prime" zurück, wenn die Zahl wahrscheinlich eine Primzahl ist, und "composite", wenn
                die Zahl definitiv keine Primzahl ist.
    >>> is_prim_millerrabin(13)
    'probably prime'
    >>> is_prim_millerrabin(105)
    'composite'
    >>> is_prim_millerrabin(89)
    'probably prime'
    >>> is_prim_millerrabin(221)
    'composite'
    """
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n < 2:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break

        else:
            return "composite"

    return "probably prime"


def is_prim(n):
    """
    Überprüft, ob die gegebene Zahl eine Primzahl ist. Indem sie sie durch die ersten 100 Primzahlen teilt und den
    Miller-Rabin-Test anwendet.
    :param number: Die zu überprüfende Zahl.
    :return: True, wenn die Zahl eine Primzahl ist, False sonst.
    >>> is_prim(2)
    True
    """
    for p in FIRST_100_PRIMES:
        if n % p == 0:
            return n == p
    return is_prim_millerrabin(n) == "probably prime"
