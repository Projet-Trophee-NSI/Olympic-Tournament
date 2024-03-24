### Importation ###
import hashlib

def hash(password: str) -> str:
    """
    Procédure qui renvoie la chaîne de caractère 'password' encodée
    en sha256 sous la forme d'une chaîne de caractère.

    Args:
        password (str): la chaîne de caractère à encoder

    Returns:
        str: la chaîne de caractère encodée
    """
    ## Précondition (début) ##
    assert(type(password) == str), "Erreur de type pour 'password' (requis: str)"
    ## Précondition (fin) ##
    
    ## Encodage de la chaîne de caractère (début) ##
    h = hashlib.new("SHA256") # Choix du type d'encodage
    h.update(password.encode()) # Encodage
    hashedPassword = h.hexdigest() # Conversion en chaîne de caractère
    ## Encodage de la chaîne de caractère (fin) ##
    
    return(hashedPassword) # Renvoie du mot de passe encodé

