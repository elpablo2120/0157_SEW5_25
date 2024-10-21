"""
__author__ = "Paul Waldecker"
__email__ = "0157@htl.rennweg.at"
__version__ = "1.0"
__copyright__ = "Copyright 2024"
__license__ = "GPL"
__status__ = "Ready to Review"
"""
import argparse
import logging
import os
import pickle
import random
from pathlib import Path

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
    """
    Generiert einen öffentlichen und privaten Schlüssel.
    :param bits: Länge des Schlüssels in Bits
    :return: public_key, private_key mit Schlüssel, N und Bitlänge vom Schlüssel
    """
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
    Liesst eine Datei und gibt die Bytes als Integer zurück.
    :param filename: Name der Datei.
    :param bytelength: Anzahl der Bytes, die gelesen werden sollen.
    :return: Generator für die Bytes der Datei.
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


def save_key(key, filename):
    """Speichert den Schlüssel (öffentlich oder privat) in einer Datei mit pickle."""
    with open(filename, 'wb') as f:
        pickle.dump(key, f)


def load_key(filename):
    """Laedt den Schlüssel (öffentlich oder privat) aus einer Datei mit pickle."""
    with open(filename, 'rb') as f:
        return pickle.load(f)


def main():
    parser = argparse.ArgumentParser(description="RSA Encryption/Decryption Tool")

    parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-k", "--keygen", help="generate new RSA keys with the given bit length", type=int)
    group.add_argument("-e", "--encrypt", help="encrypt a file")
    group.add_argument("-d", "--decrypt", help="decrypt a file")

    args = parser.parse_args()

    if args.verbosity:
        logging.basicConfig(level=logging.INFO)
        logging.info("Verbosity turned on")

    # Key generation
    if args.keygen:
        logging.info(f"Generating RSA keys of length {args.keygen} bits...")
        private_key, public_key = generate_keys(args.keygen)

        # Save the keys
        save_key(private_key, 'private_key.pem')
        save_key(public_key, 'public_key.pem')
        logging.info(f"Keys saved to 'private_key.pem' and 'public_key.pem'.")

    # File encryption
    elif args.encrypt:
        logging.info(f"Encrypting file: {args.encrypt}")
        if not Path("public_key.pem").is_file():
            logging.error("Public key not found. Please generate keys first.")
            return

        public_key = load_key('public_key.pem')
        output_file = args.encrypt + ".enc"
        encryptFile(args.encrypt, output_file, public_key)
        logging.info(f"File encrypted to: {output_file}")

    # File decryption
    elif args.decrypt:
        logging.info(f"Decrypting file: {args.decrypt}")
        if not Path("private_key.pem").is_file():
            logging.error("Private key not found. Please generate keys first.")
            return

        private_key = load_key('private_key.pem')
        output_file = args.decrypt.replace(".enc", ".dec")  # Removing the .enc extension
        decryptFile(args.decrypt, output_file, private_key)
        logging.info(f"File decrypted to: {output_file}")


if __name__ == "__main__":
    # private_key, public_key = generate_keys(1024)
    # print(f"Private key: {private_key[0].bit_length()}")
    # print(f"Public key: {public_key[0].bit_length()}")
    # print(f"Private key bit length: {private_key[2]}")
    # print(f"Public key bit length: {public_key[2]}")
    # print(f"n bit length: {public_key[1].bit_length()}")

    # encryptFile("test.txt", "test_encrypted.txt", public_key)
    # decryptFile("test_encrypted.txt", "test_decrypted.txt", private_key)

    main()
