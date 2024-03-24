import requests

def getIpAddress():
    url = 'https://api.ipify.org'
    response = requests.get(url)
    ipAddress = response.text
    return(ipAddress)