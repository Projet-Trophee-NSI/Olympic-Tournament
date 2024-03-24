### Importation ###
import requests

def getIpAddress() -> str:
    """
    Fonction qui renvoie l'adresse IP (internet) de la machine sur laquelle l'utilisateur est connecté

    Returns:
        str: l'adresse IP de l'utilisateur
    """
    url = 'https://api.ipify.org'
    response = requests.get(url)
    ipAddress = response.text
    return(ipAddress)