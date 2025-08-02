import string
import secrets
from app.models import URLEntries


def generate_short_url(length=6):
    character = string.ascii_uppercase + string.ascii_lowercase + string.digits 

    string_char = "".join(secrets.choice(character) for _ in range(length))

    while URLEntries.query.filter_by(short_url=string_char).first():
        string_char = "".join(secrets.choice(character) for _ in range(length))

    return string_char


# print(generate_short_url())