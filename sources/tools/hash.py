import hashlib  ### importation du module hashlib

def hash(password: str) -> str:
    """
    Procédure qui renvoie la chaîne de caractère 'password' encodée
    en sha256 sous la forme d'une chaîne de caractère.

    Args:
        password (str): la chaîne de caractère à encoder

    Returns:
        str: la chaîne de caractère encodée
    """
    assert(type(password) == str), "Erreur de type pour 'password' (requis: str)"
    h = hashlib.new("SHA256")
    h.update(password.encode())
    password_hash = h.hexdigest()
    return password_hash

