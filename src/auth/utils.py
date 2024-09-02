import bcrypt


def hash_password(password: str):
    """Генерация хэша пароля"""
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)
