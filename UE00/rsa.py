import random

import miller_rabin
import math


def ggt(x: int, y: int) -> int:
    """
    Berechnet den größten gemeinsamen Teiler von x und y.
    :param x: Zahl 1
    :param y: Zahl 2
    :return: größter gemeinsamer Teiler der beiden Zahlen
    >>> ggt(12, 15)
    3
    >>> ggt(12, 0)
    12
    >>> ggt(0, 15)
    15
    """
    while y != 0:
        x, y = y, x % y
    return x


def generate_keys(bits):
    while True:
        p = miller_rabin.generate_prime(math.ceil(bits / 2) + 1)
        q = miller_rabin.generate_prime(bits // 2)
        n = p * q
        if n.bit_length() > bits:
            break

    phi_n = (p - 1) * (q - 1)
    e = random.getrandbits(bits)
    g = ggt(e, phi_n)
    while g != 1:
        e = random.getrandbits(bits)
        g = ggt(e, phi_n)

    d = pow(e, -1, phi_n)

    public_key = (e, n, e.bit_length())
    private_key = (d, n, d.bit_length())

    return public_key, private_key


if __name__ == "__main__":

    private_key, public_key = generate_keys(1024)
    print(f"Private key: {private_key[0].bit_length()}")
    print(f"Public key: {public_key[0].bit_length()}")
    print(f"Private key bit length: {private_key[2]}")
    print(f"Public key bit length: {public_key[2]}")
    print(f"n bit length: {public_key[1].bit_length()}")

