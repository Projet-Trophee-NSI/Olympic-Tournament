### Importation ###
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
import os

localPath = os.path.dirname(os.path.abspath(__file__))

def displayMessageBox(typeOfMessage: int, title: str, text: str) -> None:
    """
    Procédure qui affiche un QMessageBox en fonction des paramètres saisis 

    Args:
        typeOfMessage (int): le type du QMessageBox
                                1 -> question
                                2 -> information
                                3 -> faire attention
                                4 -> situation bloquante
        title (str): le titre de la fenêtre
        text (str): le texte contenu dans la fenêtre
    """
    ## Préconditions (début) ##
    assert(type(typeOfMessage) == int), "Erreur de type pour 'typeOfMessage' (requis: int)"
    assert(type(title) == str), "Erreur de type pour 'title' (requis: str)"
    assert(type(text) == str), "Erreur de type pour 'text' (requis: str)"
    ## Préconditions (fin) ##
    
    ## Création de la boîte de message (début) ##
    msgBox = QMessageBox()
    msgBox.setWindowIcon(QIcon(localPath + "/../ressources/mainLogo.jpg"))
    msgBox.setWindowTitle(title)
    msgBox.setText(text)
    ## Création de la boîte de message (fin) ##
    
    ## Configuration de la boîte de message (début) ##
    if(typeOfMessage == 1):
        msgBox.setIcon(QMessageBox.Question)
    elif(typeOfMessage == 2):
        msgBox.setIcon(QMessageBox.Information)
    elif(typeOfMessage == 3):
        msgBox.setIcon(QMessageBox.Warning)
    elif(typeOfMessage == 4):
        msgBox.setIcon(QMessageBox.Critical)
    ## Configuration de la boîte de message (fin) ##
    
    msgBox.exec_() # Exécution de la boîte de message