import pandas as pd
import unicodedata
import secrets
import os
import logging
import argparse
from logging.handlers import RotatingFileHandler

# Argument parser setup
parser = argparse.ArgumentParser(description="Create class users from an Excel file.")
parser.add_argument("input_file", help="Path to the input Excel file")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
parser.add_argument("-q", "--quiet", action="store_true", help="Enable quiet logging")
args = parser.parse_args()

# Logging configuration
log_file = "./output/create_class.log"
os.makedirs("./output", exist_ok=True)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG if args.verbose else logging.WARNING if args.quiet else logging.INFO)

handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

def normalize_username(name: str) -> str:
    name = name.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    name = unicodedata.normalize("NFD", name)
    name = ''.join(c for c in name if not unicodedata.combining(c))
    name = name.lower().replace(" ", "_")
    return ''.join(c for c in name if c.isalnum() or c == "_")

def generate_password_student(class_name, room_number, advisor) -> str:
    special_chars = "!%&(),._-=^#"
    random_char = secrets.choice(special_chars)
    return f"{class_name[0]}{random_char}{room_number[:3]}{advisor[0].upper()}"

def generate_password_teacher_seminar(length=12) -> str:
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!%&(),._-=^#"
    return ''.join(secrets.choice(chars) for _ in range(length))

if __name__ == "__main__":


