import hashlib  ### importation du module hashlib

def hash(password : str) -> str:
    """
    Renvoie la chaîne de caractère mdp encodée en sha256 sous la forme d'une chaîne de caractère
    """
    assert(type(password) == str), "Erreur de type pour 'password' (requis: str)"
    h = hashlib.new("SHA256")
    h.update(password.encode())
    password_hash = h.hexdigest()
    return password_hash

