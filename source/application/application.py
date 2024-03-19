from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QListWidget, QLineEdit, QFileDialog
from PyQt5.QtGui import QPixmap, QIcon, QColor, QBrush
from PyQt5.QtCore import Qt, QDate, QSize
from PyQt5.uic import loadUi
from datetime import datetime
import os
import sys
import ctypes

localPath = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, localPath + "/../tools")
sys.path.insert(0, localPath + "/../database")

import treeGenerator
import displayMessageBox as message
import imageViewer
import createPDF
import makeRequest
import hash
import getIP

class MonApplication(QMainWindow):
    def __init__(self, idOfUser: int, typeOfUser: int, loginId: int, hashPassword: int):
        super(MonApplication, self).__init__()
        self.idOfUser = int(idOfUser)
        self.typeOfUser = int(typeOfUser)
        self.loginId = loginId
        self.hashPassword = hashPassword
        self.userName = makeRequest.getInfoPrecis(idOfUser, "nom")
        self.ipAddress = getIP.getIpAddress()
        
        self.setWindowTitle("Best tournament")
        self.setWindowIcon(QIcon(localPath + "/../ressources/mainLogo.jpg"))
        
        # Créer un widget central
        #self.windowContent = QWidget()
        #self.setCentralWidget(self.windowContent)
        
        # Charger l'interface utilisateur dans le widget central
        loadUi(localPath + "/application.ui", self)
        
        if(self.typeOfUser == 0):
            self.actionAdminPanel.setVisible(False)
            for _ in range(2): self.toolBar.removeAction(self.toolBar.actions()[-1])
        
        self.actionBrowse.setIcon(QIcon(localPath + "/../ressources/browseIcon.png"))
        self.actionCreate.setIcon(QIcon(localPath + "/../ressources/createIcon.png"))
        self.actionMyTournaments.setIcon(QIcon(localPath + "/../ressources/configureIcon.png"))
        self.actionProfile.setIcon(QIcon(localPath + "/../ressources/profileIcon.png"))
        self.actionAdminPanel.setIcon(QIcon(localPath + "/../ressources/adminPanelIcon.png"))
        self.mainIconLabel.setPixmap(QPixmap(localPath + "/../ressources/mainLogo.jpg"))
        
        sortingItems = ["Aucun", "Noms croissants", "Noms décroissant", "Sports croissants", "Sports décroissants", "Plus récent", "Plus ancien", "Tri personnalisé"]
        self.sortComboBox.addItems(sortingItems)
        
        self.roleDelComboBox.addItems(["Utilisateur", "Administrateur"])
        self.accountDelComboBox.addItems(makeRequest.getListeUser())
        
        self.actionBrowse.triggered.connect(browseTournament)
        self.actionCreate.triggered.connect(lambda: createTournament(1))
        self.actionMyTournaments.triggered.connect(manageMyTournaments)
        self.actionProfile.triggered.connect(lambda: self.userStackedWidget.setCurrentIndex(2))
        self.actionProfile.triggered.connect(lambda: self.mainStackedWidget.setCurrentIndex(0))
        self.actionAdminPanel.triggered.connect(lambda: self.mainStackedWidget.setCurrentIndex(1))
        self.hidePushButton.clicked.connect(hideTree)
        self.tableWidget.itemDoubleClicked.connect(tournamentClicked)
        self.doModificationscheckBox.toggled.connect(hideModifications)
        self.seeMyTournamentsCheckBox.toggled.connect(manageMyTournamentsSelect)
        self.sortComboBox.currentIndexChanged.connect(sortTablesElements)
        self.searchLineEdit.textChanged.connect(searchTournament)
        self.addParticipantsPushButton.clicked.connect(lambda: addParticipants())
        self.delLastElementPushButton.clicked.connect(lambda: self.participantsListListWidget.takeItem(self.participantsListListWidget.count() - 1))
        self.previewPushButton.clicked.connect(lambda: makePreview(self.participantsListListWidget))
        self.startDateEdit.dateChanged.connect(lambda _: self.endDateEdit.setMinimumDate(self.startDateEdit.date()))
        self.validateTournamentPushButton.clicked.connect(lambda: defineTournament())
        self.addArbiterPushButton.clicked.connect(lambda: addArbiter())
        self.delLastArbiterPushButton.clicked.connect(lambda: self.arbiterListWidget.takeItem(self.arbiterListWidget.count() - 1))
        self.seeNewPasswordPushButton.clicked.connect(lambda: seeNewPassword())
        self.downloadDataPushButton.clicked.connect(lambda: downloadData())
        self.updateUsernamePushButton.clicked.connect(lambda: updateProfile("nom", self.idOfUser))
        self.updateMailPushButton.clicked.connect(lambda: updateProfile("email", self.idOfUser))
        self.updateAgePushButton.clicked.connect(lambda: updateProfile("age", self.idOfUser))
        self.updatePasswordPushButton.clicked.connect(lambda: updateProfile("mdp", self.idOfUser))
        self.addPushButton.clicked.connect(lambda: getRegisterAdmin())
        self.delPushButton.clicked.connect(lambda: delUserAdmin())
        self.verificationAddCheckBox.toggled.connect(sureToAddAdmin)
        self.verificationDelCheckBox.toggled.connect(sureToDelUserAdmin)
        self.roleDelComboBox.currentIndexChanged.connect(fillAdminPanelCombobox)
        
        self.tableWidget.setSortingEnabled(True)
        
        self.startDateEdit.setMinimumDate(QDate.currentDate())
        self.endDateEdit.setMinimumDate(QDate.currentDate())
        
        self.onLogin()
        
        self.iw = imageViewer.ImageViewer()
        self.verticalLayout_7.addWidget(self.iw)
        self.iw.show()
        
        """## TEMPORAIRE
        self.iw.setPhoto(QPixmap(localPath + "/../tools/treePreview.png"))
        self.verticalLayout_7.addWidget(self.iw)
        self.iw.show()
        ## TEMPORAIRE"""
        
        self.modifyGroupBox.hide()
        
    def onLogin(self) -> None:
        """
        Procédure qui remplit l'ensemble des labels satiques de l'application et qui dépendent seulement de l'utilisateur
        """
        info = makeRequest.getInfo(self.idOfUser)[0]
        self.mailLabel.setText(self.loginId)
        self.dateLabel.setText(info[5])
        self.ageLabel.setText(str(info[4]))
        self.usernameLabel.setText(self.userName)
        
def tournamentClicked(item):
    if(item.column() == 0):
        application.playersListWidget.clear()
        test = makeRequest.getInfoTournois(item.text())[0]
        equipe = makeRequest.convertSTRtoLst(test[3])
        for e in equipe:
            application.playersListWidget.addItem(e)
        
        treeGenerator.drawBinaryTree(treeGenerator.createTree(list(equipe)), False)
        application.iw.setPhoto(QPixmap(localPath + "\\treeView.png"))
        os.remove(localPath + "\\treeView.png")
        application.tournamentNameLabel.setText(item.text())
        application.detailsTextEdit.setText(test[7])
        application.startLabel_2.setText(str(test[8]))
        application.endLabel_2.setText(str(test[9]))
        application.userStackedWidget.setCurrentIndex(1)
    else:
        filterTablesElements([item.text()])
        application.sortComboBox.setCurrentIndex(7)
        
def hideTree():
    if(application.hidePushButton.isChecked()):
        application.iw.hide()
        application.hidePushButton.setText("Montrer")
    else:
        application.iw.show()
        application.hidePushButton.setText("Cacher")

def hideModifications(state):
    if(state): application.modifyGroupBox.show()
    else: application.modifyGroupBox.hide()

def browseTournament():
    application.seeMyTournamentsCheckBox.setChecked(False)
    application.userStackedWidget.setCurrentIndex(0)
    application.mainStackedWidget.setCurrentIndex(0)

def manageMyTournaments():
    if(not(application.seeMyTournamentsCheckBox.isChecked())):
        application.seeMyTournamentsCheckBox.setChecked(True)
    application.userStackedWidget.setCurrentIndex(0)
    application.mainStackedWidget.setCurrentIndex(0)
    
def manageMyTournamentsSelect(state: bool) -> None:
    """
    Procédure qui permet l'affichage des tournois dont l'utilisateur est arbitre

    Args:
        state (bool): Etat de la case, si elle est cochée alors on filtre
    """
    if(state):
        application.tableWidget.setRowCount(0)
        liste = makeRequest.getTable("TournoiArbre")
        for tournois in liste:
            arb = tournois[2]
            crea = tournois[-1]
            if (application.userName in arb) or (application.userName==crea): 
                fillTableWidget([[tournois[1],tournois[6],tournois[8],tournois[9],tournois[-1]]])

    else: fillTournamentTable()
            
def fillTableWidget(elements: list[list[str]]) -> None:
    for i in range(len(elements)):
        application.tableWidget.insertRow(i)
        for j in range(len(elements[i])):
            if(j == 2) : item = QTableWidgetItem(str(datetime.strptime(elements[i][j], "%d/%m/%Y").date()))
            else: item = QTableWidgetItem(elements[i][j])
            item.setForeground(QBrush(QColor(255, 255, 255)))
            application.tableWidget.setItem(i, j, item)

def filterTablesElements(textList: list[str]):
    for i in range(application.tableWidget.rowCount()):
        row_match = False
        for j in range(application.tableWidget.columnCount()):
            item = application.tableWidget.item(i, j)
            # Vérifier si l'élément contient le texte recherché
            for e in textList:
                if e.lower() in item.text().lower():
                    row_match = True
                    break
        # Masquer la ligne si le texte recherché n'est pas trouvé
        application.tableWidget.setRowHidden(i, not row_match)
 
def sortTablesElements(sort: int):
    if(sort == 0):
        for i in range(application.tableWidget.rowCount()):
            application.tableWidget.setRowHidden(i, False)
    elif(sort == 1): application.tableWidget.sortItems(0, Qt.AscendingOrder)
    elif(sort == 2): application.tableWidget.sortItems(0, Qt.DescendingOrder)
    elif(sort == 3): application.tableWidget.sortItems(1, Qt.AscendingOrder)
    elif(sort == 4): application.tableWidget.sortItems(1, Qt.DescendingOrder)
    elif(sort == 5): application.tableWidget.sortItems(2, Qt.AscendingOrder)
    elif(sort == 6): application.tableWidget.sortItems(2, Qt.DescendingOrder)

def searchTournament(searchedText: str) -> None: filterTablesElements(searchedText.split())

def createTournament(mode: int) -> None:
    if(mode == 1):
        application.winnerGroupBox.hide()
        application.delTournamentGroupBox.hide()
        application.participantsGroupBox.show()
        application.createTournamentLabel.setText("Créer un nouveau tournoi")
    elif(mode == 2):
        application.winnerGroupBox.show()
        application.delTournamentGroupBox.show()
        application.participantsGroupBox.hide()
        application.createTournamentLabel.setText("Modifier un tournoi")
    
    application.arbiterNameComboBox.addItems(makeRequest.getListeUser() + makeRequest.getListeAdmin())
    application.userStackedWidget.setCurrentIndex(3)
    application.mainStackedWidget.setCurrentIndex(0)

def makePreview(list: QListWidget) -> None:
    """
    Procédure qui générère un arbre en fonction des participants entrés par l'utilisateur

    Args:
        list (QListWidget): le widget contenant l'ensemble des participants saisis par l'utilisateur
    """
    items = []
    for i in range(list.count()):
        items.append(list.item(i).text())
    
    if(len(items) >= 2):
        treeGenerator.drawBinaryTree(treeGenerator.createTree(items), True)
    else:
        message.displayMessageBox(4, "Manque de participants", "Vous avez entré moins de 2 participants à votre tournoi, la prévisualisation est impossible.")

def defineTournament() -> None:
    """
    Procédure qui récupère les informations du tournoi et les enregistre dans la base de donnée

    MANQUE : nom du créateur
    """
    name = application.tournamentNameLineEdit.text()
    activity = application.tournamentActivityLineEdit.text()
    description = application.tournamentResumeTextEdit.toPlainText()
    startDate = application.startDateEdit.date().toString('dd/MM/yyyy')
    endDate = application.endDateEdit.date().toString('dd/MM/yyyy')
    participants = [application.participantsListListWidget.item(i).text() for i in range(application.participantsListListWidget.count())]
    arbiters = [application.arbiterListWidget.item(i).text() for i in range(application.arbiterListWidget.count())]
    
    if (len(participants) < 2):
        message.displayMessageBox(4, "Manque de participants", "Vous avez entré moins de 2 participants à votre tournoi, la création est impossible.")

    elif ((len(participants)%2) != 0):
        message.displayMessageBox(4, "Manque de participants", f"Vous avez entréun nombre impaire de participants ({len(participants)}) à votre tournoi, la création est impossible.")

    else:
        if (name == "") or (activity == "") or (description == "") or (len(arbiters) < 1):
            message.displayMessageBox(4,"Manque information", "Tous les champs doivent être remplie, la création est impossible.")
        else:
            makeRequest.cree_TournoiArbre(name, arbiters, participants, activity, description, startDate, endDate, application.userName) #ajout nom créateur
            message.displayMessageBox(2, "Réussite", "Création du tournoi réussi")

    fillTableWidget([[name, activity, str(startDate), str(endDate), makeRequest.getInfo(content[0])[0][1]]])

def fillTournamentTable() -> None:
    """
    Procédure qui rempli le tableau contenant l'ensemble des tournois à partir de la base de données
    """
    liste = []
    table = makeRequest.getTable("TournoiArbre")
    for e in table:
        tournois = [e[1], e[6], e[8], e[9],e[11]]
        liste.append(tournois)

    fillTableWidget(liste)
    
def fillArbiterComboBox() -> None:
    """
    Procédure qui rempli le comboBox 'arbiterNameComboBox' contenant l'ensemble des utilisateurs à partir de la base de donnée
    A COMPLETER
    """

def addArbiter():
    arbiterName = application.arbiterNameComboBox.currentText()
    if(application.arbiterNameComboBox.findText(arbiterName) != -1):
        application.arbiterListWidget.addItem(arbiterName)
    else:
        message.displayMessageBox(4, "Arbitre inconnu", "L'utilisateur que vous essayez d'ajouter en tant qu'arbitre de votre tournoi "+
                                  "n'existe pas, veuillez en choisir un dans la liste mise à votre disposition.")

def addParticipants():
    application.participantsListListWidget.addItem(application.addParticipantsLineEdit.text())
    application.addParticipantsLineEdit.setText("")

def seeNewPassword() -> None:
    """
    Procédure permettant d'afficher/cacher le texte saisi dans le champ correspondant au nouveau mot de passe dans la page du profil
    """
    current_mode = application.changePasswordLineEdit.echoMode() #recupère le mode d'affichage actuelle  de passwordLineEdit
    new_mode = QLineEdit.Normal if current_mode == QLineEdit.Password else QLineEdit.Password #affecte un mode affichage avec : QLineEdit.Normal : Affiche le texte normalement|QLineEdit.Password : Affiche des caractères de remplacement pour masquer le texte
    application.changePasswordLineEdit.setEchoMode(new_mode) #modifie le mode de l'affichage de passwordLineEdit

def downloadData() -> None:
    userName = "Nom d'utilisateur : " + application.usernameLabel.text()
    mail = "Courrier électronique : " + application.loginId
    date = "Date de création du compte : " + application.dateLabel.text()
    age = "Âge : " + application.ageLabel.text()
    ip = "Adresse IP : " + application.ipAddress
    
    fileName, _ = QFileDialog.getSaveFileName(None,"Enregistrer mes données", "Mes donnees", "PDF Files (*.pdf)")
    
    if(fileName):
        createPDF.genDataPDF([userName, mail, date, age, ip], fileName)
        os.startfile(fileName) 
    else:
        message.displayMessageBox(3, "Enregistrement impossible", "Vos données n'ont pas pu être téléchargées car l'emplacement saisi est invalide ou inexistant.")

def updateProfile(object : str, id : int)->None:
    if object == "age":
        modif = application.changeAgeSpinBox.value()
        if makeRequest.modife_donne_user(id, modif, object) == True: application.ageLabel.setText(str(modif))
        else: message.displayMessageBox(4, "Erreur", "La modification n'a pas pu être effectuer")

    elif object == "email":
        modif = application.changeMailLineEdit.text()
        if makeRequest.modife_donne_user(id, modif, object) == True: application.mailLabel.setText(modif)
        else: message.displayMessageBox(4, "Erreur", "La modification n'a pas pu être effectuer, essayez un autre mail")

    elif object == "nom":
        modif = application.changeUsernameLineEdit.text()
        if makeRequest.modife_donne_user(id, modif, object) == True: application.usernameLabel.setText(modif)
        else: message.displayMessageBox(4, "Erreur", "La modification n'a pas pu être effectuer, essayez un autre nom")

    elif hash.hash(application.currentPasswordLineEdit.text()) == makeRequest.getInfo(id)[0][3] and object == "mdp":
        modif = hash.hash(application.changePasswordLineEdit.text())
        if makeRequest.modife_donne_user(id, modif, object) != True: message.displayMessageBox(4, "Erreur", "La modification n'a pas pu être effectuer")

    else: 
        message.displayMessageBox(4, "Mot de passe incorrect", "Votre mot de passe est incorrect.")

def getRegisterAdmin() -> None:
    """
    Procédure qui inscrit les données saisies dans la base de donnée
    """
    pseudo = application.nameAddLineEdit.text()
    email = application.mailAddLineEdit.text()
    password = application.passwordAddLineEdit.text()
    age = application.ageAddSpinBox.value()
    ip = "compte créé par '" + str(getIP.getIpAddress()) + "'"
    
    if(pseudo != "" and password != "" and email != ""):
        if makeRequest.inscri_donne(pseudo, hash.hash(password), email, age, 1, ip) == True:
            message.displayMessageBox(2, "Inscription réussie", "L'inscription est réussie, " +
                                      "vous pouvez dès maintenant donner ces identifiants au nouvel administrateur pour qu'il/elle se connecte via la page de connexion." + 
                                      "Les identifiants de connexion sont : \n- Identifiant : " + email + "\n- Mot de passe : " + password + "(à conserver secret)")
        else:
            message.displayMessageBox(4, "Erreur d'inscription", "L'inscription a échouée, le nom d'utilisateur ou le mail est probablement déjà utilisé.")
    else:
        message.displayMessageBox(4, "Informations mal complétées", "Au moins l'un des trois champs de saisie est vide, veuillez le/les remplir pour valider votre inscription.")

def delUserAdmin() -> None:
    table = makeRequest.getTable("User")
    for e in table:
        if(e[1] == application.accountDelComboBox.currentText()): makeRequest.suprime_donne_user(e[0])

def sureToAddAdmin(state: bool) -> None:
    application.addPushButton.setEnabled(state)
    if(state): application.addPushButton.setStyleSheet("color: rgb(0, 135, 0);\nbackground-color: rgb(255, 255, 255);\nborder: 2px solid white;\nborder-radius: 7px;")
    else: application.addPushButton.setStyleSheet("color: rgb(0, 135, 0);\nbackground-color: rgb(255, 255, 255);\nbackground-color: rgb(99, 99, 99);\ncolor: rgb(150, 150, 150);\nborder: 2px solid rgb(99, 99, 99);\nborder-radius: 7px;")    

def fillAdminPanelCombobox(index: int) -> None:
    application.accountDelComboBox.clear()
    if(index == 0):
        application.accountDelComboBox.addItems(makeRequest.getListeUser())
    elif(index == 1):
        application.accountDelComboBox.addItems(makeRequest.getListeAdmin())

def sureToDelUserAdmin(state: bool) -> None:
    application.delPushButton.setEnabled(state)
    if(state): application.delPushButton.setStyleSheet("color: rgb(193, 0, 0);\nbackground-color: rgb(255, 255, 255);\nborder: 2px solid white;\nborder-radius: 7px;")
    else: application.delPushButton.setStyleSheet("color: rgb(0, 135, 0);\nbackground-color: rgb(255, 255, 255);\nbackground-color: rgb(99, 99, 99);\ncolor: rgb(150, 150, 150);\nborder: 2px solid rgb(99, 99, 99);\nborder-radius: 7px;")

if __name__ == '__main__':
    app = QApplication([])
    
    ## Forcer l'icône de la barre des tâche (début) ##
    # Provient de : https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
    myappid = 'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app.setWindowIcon(QIcon(localPath + "/../ressources/mainLogo.ico"))
    ## Forcer l'icône de la barre des tâche (fin) ##
    
    with open(localPath + "/temp.tmp", 'r') as tempFile:
        content = tempFile.read()
    os.remove(localPath + "/temp.tmp")
    
    content = content.split(";")
    
    application = MonApplication(content[0], content[1], content[2], content[3])
    application.show()
    
    fillTournamentTable()
    #fillTableWidget([["Tournoi 1", "Tennis", "23/02/2024", "25/02/2024", "Antoine"], ["Tournoi 2", "Pétanque", "20/02/2024", "18/04/2024", "Jonathan"]]) # TEMPORAIRE
    
    application.sortComboBox.setCurrentIndex(0)
    application.setMinimumSize(QSize(800, 400))
    application.setMaximumSize(QSize(800, 800))
    application.resize(QSize(800, 600))
    
    app.exec_()