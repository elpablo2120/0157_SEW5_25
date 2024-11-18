"""
__author__ = "Paul Waldecker"
__email__ = "0157@htl.rennweg.at"
__version__ = "3.0"
__copyright__ = "Copyright 2024"
__license__ = "GPL"
__status__ = "Ready to Review"
"""

import unicodedata
import secrets
import os
import logging
import argparse
from logging.handlers import RotatingFileHandler
import pandas as pd


def normalize_username(name: str) -> str:
    """
    Normalisiere den Namen so, dass keine Akzente und Sonderzeichen mehr enthalten sind
    @param name: Der Name, der normalisiert werden soll
    @return: Der normalisierte Name
    >>> normalize_username("ÜÖÄüöäß()!%&")
    'ueoeaeueoeaess'
    """
    name = name.replace('ä', 'ae').replace('Ä', 'Ae').replace('ö', 'oe').replace('Ö', 'Oe').replace('ü', 'ue').replace(
        'Ü', 'Ue').replace('ß', 'ss')
    name = unicodedata.normalize("NFD", name)
    name = ''.join(c for c in name if not unicodedata.combining(c))
    name = name.lower().replace(" ", "_")
    return ''.join(c for c in name if c.isalnum() or c == "_")


def generate_password_class(class_name, room_number, advisor) -> str:
    """
    Generiere ein Passwort für Schüler im Format: KlasseZufallszeichenRaumNrKV
    @param class_name: Der Name der Klasse
    @param room_number: Die Raumnummer
    @param advisor: Der Klassenlehrer
    @return: Das generierte Passwort
    >>> generate_password_class("4A", "123", "Mustermann")
    '4!123M'
    """
    special_chars = "!%&(),._-=^#"
    random_char = secrets.choice(special_chars.replace(',', ''))
    return f"{class_name[0]}{random_char}{room_number[:3]}{advisor[0].upper()}"


def generate_password_twelve(length=12) -> str:
    """
    Generiere ein zufälliges Passwort mit einer Länge von 12 Zeichen
    @param length: Die Länge des Passworts
    @return: Das generierte Passwort
    """
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!%&(),._-=^#"
    return ''.join(secrets.choice(chars) for _ in range(length))


def main():
    parser = argparse.ArgumentParser(description="Create class users from an Excel file.")
    parser.add_argument("input_file", help="Path to the input Excel file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("-q", "--quiet", action="store_true", help="Enable quiet logging")
    args = parser.parse_args()

    # Logging Setup
    log_file = "./output/create_class.log"
    os.makedirs("./output", exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if args.verbose else logging.WARNING if args.quiet else logging.INFO)

    # RotatingFileHandler
    handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=5)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

    # StreamHandler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(stream_handler)

    try:
        class_data = pd.read_excel(args.input_file)
    except FileNotFoundError:
        logger.error(f"File not found: {args.input_file}")
        exit(1)

    add_script_path = "./output/class_add.sh"
    del_script_path = "./output/class_del.sh"
    csv_path = "./output/class.csv"

    with open(add_script_path, "w") as add_script, open(del_script_path, "w") as del_script:
        add_script.write("#!/bin/bash\n")
        del_script.write("#!/bin/bash\n")

        csv_data = []
        for _, row in (x for x in class_data.iterrows() if not pd.isnull(x[1]["Klasse"])):
            class_name = str(row["Klasse"])
            room_number = str(row["Raum Nr."])
            advisor = str(row["KV"])

            username = f"k{normalize_username(class_name)}"
            password = generate_password_class(class_name, room_number, advisor)

            home_dir = f"/home/klassen/{username}"
            groups = "cdrom,plugdev,sambashare"

            add_script.write(
                f"useradd -m -d {home_dir} -s /bin/bash -c '{username}' -G {groups} {username}\n"
                f"echo '{username}:{password}' | chpasswd\n"
            )
            del_script.write(f"userdel -r {username}\n")

            csv_data.append({"Username": username, "Password": password})

            logger.debug(
                f"Created user {username} with password {password} and home directory {home_dir} for class {class_name} in room {room_number} with advisor {advisor}.")

        for user in ["lehrer", "seminar"]:
            username = user
            password = generate_password_twelve()
            home_dir = f"/home/lehrer/{username}"

            add_script.write(
                f"useradd -m -d {home_dir} -s /bin/bash -c '{username}' -G {groups} {username}\n"
                f"echo '{username}:{password}' | chpasswd\n"
            )
            del_script.write(f"userdel -r {username}\n")

            csv_data.append({"Username": username, "Password": password})

    csv_df = pd.DataFrame(csv_data)
    csv_df.to_csv(csv_path, index=False)

    os.chmod(add_script_path, 0o755)
    os.chmod(del_script_path, 0o755)

    logger.info("Scripts class_add.sh, class_del.sh, and class.csv successfully created.")


if __name__ == "__main__":
    main()
