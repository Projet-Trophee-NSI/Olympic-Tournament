### Importation ###
import requests

def getIpAddress() -> str:
    """
    Fonction qui renvoie l'adresse IP (internet) de la machine sur laquelle l'utilisateur est connecté

    Returns:
        str: l'adresse IP de l'utilisateur
    """
    ## Récupération de l'adresse IP (début) ##
    url = 'https://api.ipify.org' # Service affichant l'adresse IP internet
    response = requests.get(url) # Récupération du contenu de la page de l'url
    ipAddress = response.text # Conversion de l'adresse IP en chaîne de caractère
    ## Récupération de l'adresse IP (fin) ##
    
    return(ipAddress) # Renvoie de l'adresse IP