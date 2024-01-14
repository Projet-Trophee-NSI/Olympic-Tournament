from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.uic import loadUi
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

localPath = os.path.dirname(os.path.abspath(__file__))

class MonApplication(QMainWindow):
    def __init__(self):
        super(MonApplication, self).__init__() #<- comprend pas le super
        
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
        self.windowContent.connectPushButton.clicked.connect(getIdPassword)
        self.windowContent.seePasswordPushButton.clicked.connect(seePasswordPage1)
        self.windowContent.seePasswordPushButtonPage2.clicked.connect(seePasswordPage2)
        self.windowContent.registrationPushButton.clicked.connect(lambda: fenetre.windowContent.stackedWidget.setCurrentIndex(1))
        self.windowContent.backPushButtonPage2.clicked.connect(lambda: fenetre.windowContent.stackedWidget.setCurrentIndex(0))
        self.windowContent.forgottenPasswordPushButton.clicked.connect(lambda: fenetre.windowContent.stackedWidget.setCurrentIndex(2))
        self.windowContent.backPushButtonPage3.clicked.connect(lambda: fenetre.windowContent.stackedWidget.setCurrentIndex(0))
        self.windowContent.acceptAgeCheckBoxPage2.toggled.connect(checkConditions)
        self.windowContent.acceptCheckBoxPage2.toggled.connect(checkConditions)
        self.windowContent.ageSpinBoxPage2.valueChanged.connect(checkConditions)
        self.windowContent.registrationPushButtonPage2.clicked.connect(getRegister)
        self.windowContent.emailPushButtonPage3.clicked.connect(sendEmail)
        ## Connexion des bouton avec leurs fonctions respectives (fin) ##

def getIdPassword():
    """
    Fonction qui renvoie l'identifiant et le mot de passe saisis par l'utilisateur
    """
    id = fenetre.windowContent.idLineEdit.text() #affecte à id le texte de l'entrer de texte idLineEdit
    password = fenetre.windowContent.passwordLineEdit.text()
    print(id, password)
    return(id, password)

def seePasswordPage1():
    """
    Procédure permettant d'afficher/cacher le texte saisi dans le champ correspondant au mot de passe de la page de connexion
    """
    current_mode = fenetre.windowContent.passwordLineEdit.echoMode() #recupère le mode d'affichage actuelle  de passwordLineEdit
    new_mode = QLineEdit.Normal if current_mode == QLineEdit.Password else QLineEdit.Password #affecte un mode affichage avec : QLineEdit.Normal : Affiche le texte normalement|QLineEdit.Password : Affiche des caractères de remplacement pour masquer le texte
    fenetre.windowContent.passwordLineEdit.setEchoMode(new_mode) #modifie le mode de l'affichage de passwordLineEdit
    
def seePasswordPage2():
    """
    Procédure permettant d'afficher/cacher le texte saisi dans le champ correspondant au mot de passe de la page de connexion
    """
    current_mode = fenetre.windowContent.passwordLineEditPage2.echoMode() #recupère le mode d'affichage actuelle  de passwordLineEdit
    new_mode = QLineEdit.Normal if current_mode == QLineEdit.Password else QLineEdit.Password #affecte un mode affichage avec : QLineEdit.Normal : Affiche le texte normalement|QLineEdit.Password : Affiche des caractères de remplacement pour masquer le texte
    fenetre.windowContent.passwordLineEditPage2.setEchoMode(new_mode) #modifie le mode de l'affichage de passwordLineEdit   

def checkConditions():
    if(fenetre.windowContent.acceptAgeCheckBoxPage2.isChecked() and fenetre.windowContent.acceptCheckBoxPage2.isChecked() and (getAge() >= 18)):
        fenetre.windowContent.registrationPushButtonPage2.setEnabled(True)
        fenetre.windowContent.registrationPushButtonPage2.setStyleSheet("color: rgb(0, 0, 0);\nbackground-color: rgb(255, 255, 255);\nborder: 2px solid white;\nborder-radius: 7px;")

    else:
        fenetre.windowContent.registrationPushButtonPage2.setEnabled(False)
        fenetre.windowContent.registrationPushButtonPage2.setStyleSheet("color: rgb(0, 0, 0);\nbackground-color: rgb(255, 255, 255);\nborder: 2px solid white;\nborder-radius: 7px;\nbackground-color: rgb(99, 99, 99);\nborder: 2px solid rgb(2, 20, 56);")

def getAge():
    age = fenetre.windowContent.ageSpinBoxPage2.value()
    print(age)
    return (age)

def getRegister():
    pseudo = fenetre.windowContent.pseudoLineEditPage2.text()
    password = fenetre.windowContent.passwordLineEditPage2.text()
    e_mail = fenetre.windowContent.idLineEditPage2.text()
    print(pseudo, e_mail, password)
    return (pseudo, e_mail, password)

def sendEmail():
    mail = fenetre.windowContent.emailLineEditPage3.text()

    # Paramètres du serveur SMTP
    smtp_server = "smtp.free.fr"
    smtp_port = 587
    smtp_username = "titouan.dorier@free.fr"
    smtp_password = "non"

    # Destinataire et expéditeur
    from_address = smtp_username
    to_address = mail

    # Création du message
    subject = "teste appli envoie mail"
    body = "Eureka ça marche\nTu as vu ça Antoine ??"
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



if __name__ == '__main__': #<- comprend pas
    app = QApplication([]) #<- comprend pas
    fenetre = MonApplication()
    fenetre.setFixedSize(348, 505)
    fenetre.show() 
    app.exec_()
