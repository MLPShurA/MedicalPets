import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    try:
        # bcrypt hashes start with $2b$, $2a$, or $2y$
        if hashed.startswith("$2"):
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        else:
            # Comparación directa si es una contraseña antigua
            return password == hashed
    except Exception as e:
        return False
