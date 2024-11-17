import secrets
import unicodedata

def normalize_username(name: str) -> str:
    name = name.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    name = unicodedata.normalize("NFD", name)
    name = ''.join(c for c in name if not unicodedata.combining(c))
    name = name.lower().replace(" ", "_")
    return ''.join(c for c in name if c.isalnum() or c == "_")

#def generate_password(class_name, room_number, advisor) -> str:
 #   special_chars = "!%&(),._-=^#"
  #  random_char = secrets.choice(special_chars)
   # return f"{class_name[0]}{random_char}{room_number[:3]}{advisor[0].upper()}"

def generate_random_password(length=12) -> str:
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!%&(),._-=^#"
    return ''.join(secrets.choice(chars) for _ in range(length))

if __name__ == "__main__":
    print(normalize_username("Hàns üßöä"))
    print(generate_random_password())

