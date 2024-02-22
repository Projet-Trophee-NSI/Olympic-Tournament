from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.uic import loadUi
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ctypes

localPath = os.path.dirname(os.path.abspath(__file__))

###import makeRequest

sys.path.insert(0, localPath + "/../database")
sys.path.insert(0, localPath + "/../tools")

import makeRequest
import hash


class MonApplication(QMainWindow):
    def __init__(self):
        super(MonApplication, self).__init__()
        
        self.setWindowTitle("Page de connexion")
        self.setWindowIcon(QIcon(localPath + "/../ressources/mainLogo.jpg"))
        
        # Créer un widget central
        self.windowContent = QWidget()
        self.setCentralWidget(self.windowContent)

        # Charger l'interface utilisateur dans le widget central
        loadUi(localPath + "/connectApp.ui", self.windowContent)
        
        ## Ajout de l'image principale sur chaque page (début) ##
        self.windowContent.mainAppLogoLabelPage1.setPixmap(QPixmap(localPath + "/../ressources/mainLogo.jpg"))
        self.windowContent.mainAppLogoLabelPage2.setPixmap(QPixmap(localPath + "/../ressources/mainLogo.jpg"))
        self.windowContent.mainAppLogoLabelPage3.setPixmap(QPixmap(localPath + "/../ressources/mainLogo.jpg"))
        ## Ajout de l'image principale sur chaque page (fin) ##
        
        self.windowContent.registrationPushButtonPage2.setEnabled(False)
        self.windowContent.registrationPushButtonPage2.setStyleSheet("color: rgb(0, 0, 0);\nbackground-color: rgb(255, 255, 255);\nborder: 2px solid white;\nborder-radius: 7px;\nbackground-color: rgb(99, 99, 99);\nborder: 2px solid rgb(2, 20, 56);")
        
        ## Connexion des bouton avec leurs fonctions respectives (début) ##
        self.windowContent.connectPushButton.clicked.connect(connectApp)
        self.windowContent.seePasswordPushButton.clicked.connect(seePasswordPage1)
        self.windowContent.seePasswordPushButtonPage2.clicked.connect(seePasswordPage2)
        self.windowContent.registrationPushButton.clicked.connect(lambda: connectAppWindow.windowContent.stackedWidget.setCurrentIndex(1))
        self.windowContent.backPushButtonPage2.clicked.connect(lambda: connectAppWindow.windowContent.stackedWidget.setCurrentIndex(0))
        self.windowContent.forgottenPasswordPushButton.clicked.connect(lambda: connectAppWindow.windowContent.stackedWidget.setCurrentIndex(2))
        self.windowContent.backPushButtonPage3.clicked.connect(lambda: connectAppWindow.windowContent.stackedWidget.setCurrentIndex(0))
        self.windowContent.acceptAgeCheckBoxPage2.toggled.connect(checkConditions)
        self.windowContent.acceptCheckBoxPage2.toggled.connect(checkConditions)
        self.windowContent.ageSpinBoxPage2.valueChanged.connect(checkConditions)
        self.windowContent.registrationPushButtonPage2.clicked.connect(getRegister)
        self.windowContent.emailPushButtonPage3.clicked.connect(sendEmail)
        ## Connexion des bouton avec leurs fonctions respectives (fin) ##

def getIdPassword() -> tuple:
    """
    Fonction qui renvoie l'identifiant et le mot de passe saisis par l'utilisateur
    """
    id_ = connectAppWindow.windowContent.idLineEdit.text() #affecte à id le texte de l'entrer de texte idLineEdit
    password = connectAppWindow.windowContent.passwordLineEdit.text()
    return(id_, password)

def seePasswordPage1() -> None:
    """
    Procédure permettant d'afficher/cacher le texte saisi dans le champ correspondant au mot de passe de la page de connexion
    """
    current_mode = connectAppWindow.windowContent.passwordLineEdit.echoMode() #recupère le mode d'affichage actuelle  de passwordLineEdit
    new_mode = QLineEdit.Normal if current_mode == QLineEdit.Password else QLineEdit.Password #affecte un mode affichage avec : QLineEdit.Normal : Affiche le texte normalement|QLineEdit.Password : Affiche des caractères de remplacement pour masquer le texte
    connectAppWindow.windowContent.passwordLineEdit.setEchoMode(new_mode) #modifie le mode de l'affichage de passwordLineEdit
    
def seePasswordPage2() -> None:
    """
    Procédure permettant d'afficher/cacher le texte saisi dans le champ correspondant au mot de passe de la page de connexion
    """
    current_mode = connectAppWindow.windowContent.passwordLineEditPage2.echoMode() #recupère le mode d'affichage actuelle  de passwordLineEdit
    new_mode = QLineEdit.Normal if current_mode == QLineEdit.Password else QLineEdit.Password #affecte un mode affichage avec : QLineEdit.Normal : Affiche le texte normalement|QLineEdit.Password : Affiche des caractères de remplacement pour masquer le texte
    connectAppWindow.windowContent.passwordLineEditPage2.setEchoMode(new_mode) #modifie le mode de l'affichage de passwordLineEdit   

def checkConditions() -> None:
    """
    Procédure vérifiant si les deux checkBox nécéssaires sont cochées pour auoriser l'inscription en rendant le bouton cliquable
    """
    if(connectAppWindow.windowContent.acceptAgeCheckBoxPage2.isChecked() and connectAppWindow.windowContent.acceptCheckBoxPage2.isChecked() and (getAge() >= 18)):
        connectAppWindow.windowContent.registrationPushButtonPage2.setEnabled(True)
        connectAppWindow.windowContent.registrationPushButtonPage2.setStyleSheet("color: rgb(0, 0, 0);\nbackground-color: rgb(255, 255, 255);\nborder: 2px solid white;\nborder-radius: 7px;")

    else:
        connectAppWindow.windowContent.registrationPushButtonPage2.setEnabled(False)
        connectAppWindow.windowContent.registrationPushButtonPage2.setStyleSheet("color: rgb(0, 0, 0);\nbackground-color: rgb(255, 255, 255);\nborder: 2px solid white;\nborder-radius: 7px;\nbackground-color: rgb(99, 99, 99);\nborder: 2px solid rgb(2, 20, 56);")

def getAge() -> int:
    """
    Fonction qui renvoie l'âge entré par l'utilisateur dans le spinBox

    Returns:
        int: correspond à l'âge entré par l'utilisateur dans le spinBox
    """
    age = connectAppWindow.windowContent.ageSpinBoxPage2.value()
    return (age)

def getRegister() -> None:
    """
    Procédure qui inscrit les données saisies dans la base de donnée
    """
    pseudo = connectAppWindow.windowContent.pseudoLineEditPage2.text()
    password = connectAppWindow.windowContent.passwordLineEditPage2.text()
    email = connectAppWindow.windowContent.idLineEditPage2.text()
    
    if(pseudo != "" and password != "" and email != ""):
        if makeRequest.inscri_donne(pseudo, hash.hash(password), email) == True:
            displayMessageBox(2, "Inscription réussie", "Votre inscription est réussie, vous pouvez dès maintenant vous connecter via la page de connexion.")
        else:
            displayMessageBox(4, "Erreur d'inscription", "Votre inscription a échouée, le nom d'utilisateur ou le mail est probablement déjà utilisé.")
    else:
        displayMessageBox(4, "Informations mal complétées", "Au moins l'un des trois champs de saisie est vide, veuillez le/les remplir pour valider votre inscription.")

def sendEmail() -> None:
    mail = connectAppWindow.windowContent.emailLineEditPage3.text()

    # Paramètres du serveur SMTP
    smtp_server = "smtp.free.fr"
    smtp_port = 587
    smtp_username = "..."
    smtp_password = "..."

    # Destinataire et expéditeur
    from_address = smtp_username
    to_address = mail

    # Création du message
    subject = "subject"
    body = "body"
    message = MIMEMultipart()
    message['From'] = from_address
    message['To'] = to_address
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Connexion au serveur SMTP
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        #server.starttls()  # Utiliser cette ligne si vous utilisez TLS
        server.login(smtp_username, smtp_password)
        
        # Envoi du message
        server.sendmail(from_address, to_address, message.as_string())
    print(mail)

def connectApp() -> None:
    """
    Procédure qui gère la connexion à l'application, si les données saisies sont correctes, on ferme la fenêtre de connexion et on lance l'application
    """
    con = getIdPassword()
    requestResult = makeRequest.connect(hash.hash(con[1]), con[0])
    print(requestResult)
    if requestResult[0] == True:
        tempConnectionFile = open(localPath + "/../application/temp.tmp", "w")
        tempConnectionFile.write(str(requestResult[1]) + ";" + str(requestResult[2])) ## RAJOUTER MAIL
        tempConnectionFile.close()
        connectAppWindow.close()
    else:
        displayMessageBox(4, "Echec de la connexion", "Vos informations sont incorrectes, vérifiez votre identifiant et votre mot de passe.")

def displayMessageBox(typeOfMessage: int, title: str, text: str) -> None:
    """
    Procédure qui affiche un QMessageBox en fonction des paramètres saisies 

    Args:
        typeOfMessage (int): le type du QMessageBox
                                1 -> question
                                2 -> information
                                3 -> faire attention
                                4 -> situation bloquante
        title (str): le titre de la fenêtre
        text (str): le texte contenu dans la fenêtre
    """
    assert(type(typeOfMessage) == int), "Erreur de type pour 'typeOfMessage' (requis: int)"
    assert(type(title) == str), "Erreur de type pour 'title' (requis: str)"
    assert(type(text) == str), "Erreur de type pour 'text' (requis: str)"
    
    msgBox = QMessageBox()
    msgBox.setWindowIcon(QIcon(localPath + "/../ressources/mainLogo.jpg"))
    msgBox.setWindowTitle(title)
    msgBox.setText(text)
    
    if(typeOfMessage == 1):
        msgBox.setIcon(QMessageBox.Question)
    elif(typeOfMessage == 2):
        msgBox.setIcon(QMessageBox.Information)
    elif(typeOfMessage == 3):
        msgBox.setIcon(QMessageBox.Warning)
    elif(typeOfMessage == 4):
        msgBox.setIcon(QMessageBox.Critical)
    
    msgBox.exec_()

if __name__ == '__main__':
    os.system("cls")
    app = QApplication([])
    
    ## Forcer l'icône de la barre des tâche (début) ##
    # Provient de : https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
    myappid = 'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app.setWindowIcon(QIcon(localPath + "/../ressources/mainLogo.ico"))
    ## Forcer l'icône de la barre des tâche (fin) ##
    
    connectAppWindow = MonApplication()
    connectAppWindow.setFixedSize(348, 505)
    connectAppWindow.show() 
    app.exec_()
