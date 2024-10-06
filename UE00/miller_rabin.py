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

    :param n: Die zu überprüfende Zahl.
    :return: True, wenn die Zahl eine Primzahl ist, False sonst.
    >>> is_prim(2)
    True
    >>> is_prim(13)
    True
    >>> is_prim(541)
    True
    >>> is_prim(543)
    False
    >>> is_prim(643)
    True
    """
    for p in FIRST_100_PRIMES:
        if n % p == 0:
            return n == p
    return is_prim_millerrabin(n) == "probably prime"


def generate_prime(bits):
    """
    Generiert eine Primzahl mit der gegebenen Bitlänge. Überprüfung durch is_prim.

    :param bits: Länge der Primzahl in Bits.
    :return: Primzahl mit der gegebenen Bitlänge, die mit 1 beginnt und endet.
    >>> n = generate_prime(4)
    >>> len(bin(n)[2:]) == 4
    True
    >>> n = generate_prime(1024)
    >>> len(bin(n)[2:]) == 1024
    True
    """
    while True:
        n = random.getrandbits(bits) | 1 << (bits - 1) | 1
        if is_prim(n):
            return n


if __name__ == "__main__":
    number = pow(2, 512) + 1
    while not is_prim(number):
        number += 2
    print(f"\nErste Primzahl mit mehr als 512 Bits: {number} \n")

    number_to_test = 24566544301293569
    if is_prim(number_to_test):
        print(f"{number_to_test} ist eine Primzahl. \n")
    else:
        print(f"{number_to_test} ist keine Primzahl. \n")

    print("\nVersteckte Nachricht in 24566544301293569 als Binärzahl mit 12 Zeichen/Zeile:")
    binary = bin(24566544301293569)[2:]
    for i in range(0, len(binary), 12):
        print(binary[i:i + 12])

    print("\nVersteckte Nachricht in 24566544301293569 als ASCII-Zeichen:")
    ascii = "".join([chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8)])
    print(ascii)

    print("\nNächst höhere Primzahl von 24566544301293569:")
    prime_higher = 24566544301293570
    while not is_prim(prime_higher):
        prime_higher += 1
    print(prime_higher)

    print("\nVersteckte Nachricht in nächst höhere Prim als Binärzahl mot 12 Zeichen/Zeile:")
    binary = bin(24566544301293587)[2:]
    for i in range(0, len(binary), 12):
        print(binary[i:i + 12])

    print("\nVersteckte Nachricht in nächst höhere Prim als ASCII-Zeichen:")
    ascii = "".join([chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8)])
    print(ascii)
