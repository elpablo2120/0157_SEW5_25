"""
__author__ = "Paul Waldecker"
__email__ = "0157@htl.rennweg.at"
__version__ = "1.0"
__copyright__ = "Copyright 2024"
__license__ = "GPL"
__status__ = "In Progress"
"""
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


def generate_keys(bits: int):
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

def file2ints(filename, bytelength):
    """
    Reads a file and converts it to a list of integers.
    :param filename: The name of the file.
    :return: A list of integers.
    """
    with open(filename, "rb") as file:
        while (byte := file.read(bytelength)):
            yield int.from_bytes(byte, byteorder="big")


def ints2file(filename, ints, bytelength):
    """
    Writes a list of integers to a file.
    :param filename: The name of the file.
    :param ints: The list of integers.
    :param bytelength: The byte length used for each integer.
    """
    with open(filename, "ab") as file:
        for i in ints:
            # Convert integer to bytes and remove leading null bytes before writing
            byte_data = i.to_bytes(bytelength, byteorder="big").lstrip(b'\x00')
            file.write(byte_data)


def encryptFile(clearfile, cryptfile, public_key):
    """
    Encrypts a message using the public key.
    :param m: The message to encrypt.
    :param public_key: The public key.
    :return: The encrypted message.
    """
    with open(cryptfile, "w") as file:
        file.write("")
    for i in file2ints(clearfile, public_key[1].bit_length() // 8):
        ints2file(cryptfile, [pow(i, public_key[0], public_key[1])], public_key[1].bit_length() // 8 + 1)

def decryptFile(cryptfile, clearfile, private_key):
    """
    Encrypts a message using the public key.
    :param m: The message to encrypt.
    :param public_key: The public key.
    :return: The encrypted message.
    """
    with open(clearfile, "w") as file:
        file.write("")
    for i in file2ints(cryptfile, private_key[1].bit_length() // 8 + 1):
        ints2file(clearfile, [pow(i, private_key[0], private_key[1])], private_key[1].bit_length() // 8)




if __name__ == "__main__":
    private_key, public_key = generate_keys(1024)
    print(f"Private key: {private_key[0].bit_length()}")
    print(f"Public key: {public_key[0].bit_length()}")
    print(f"Private key bit length: {private_key[2]}")
    print(f"Public key bit length: {public_key[2]}")
    print(f"n bit length: {public_key[1].bit_length()}")

    encryptFile("test.txt", "test_encrypted.txt", public_key)
    decryptFile("test_encrypted.txt", "test_decrypted.txt", private_key)
