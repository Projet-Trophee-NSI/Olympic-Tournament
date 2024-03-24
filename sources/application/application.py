### Importation ###
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
        
        loadUi(localPath + "/application.ui", self) # Chargement de l'interface
        
        ## Configuration de la fenêtre en fonction du type d'utilisateur (début) ##
        if(self.typeOfUser == 0):
            self.actionAdminPanel.setVisible(False)
            for _ in range(2): self.toolBar.removeAction(self.toolBar.actions()[-1])
        ## Configuration de la fenêtre en fonction du type d'utilisateur (fin) ##
        
        ## Définition des icônes (début) ##
        self.actionBrowse.setIcon(QIcon(localPath + "/../ressources/browseIcon.png"))
        self.actionCreate.setIcon(QIcon(localPath + "/../ressources/createIcon.png"))
        self.actionMyTournaments.setIcon(QIcon(localPath + "/../ressources/configureIcon.png"))
        self.actionProfile.setIcon(QIcon(localPath + "/../ressources/profileIcon.png"))
        self.actionAdminPanel.setIcon(QIcon(localPath + "/../ressources/adminPanelIcon.png"))
        self.mainIconLabel.setPixmap(QPixmap(localPath + "/../ressources/mainLogo.jpg"))
        ## Définition des icônes (fin) ##
        
        sortingItems = ["Aucun", "Noms croissants", "Noms décroissant", "Sports croissants", "Sports décroissants", "Plus récent", "Plus ancien", "Tri personnalisé"]
        self.sortComboBox.addItems(sortingItems)
        
        self.roleDelComboBox.addItems(["Utilisateur", "Administrateur"])
        self.accountDelComboBox.addItems(makeRequest.getListeUser())
        
        ## Création d'un lien entre les boutons et leur action (début) ##
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
        self.configurePushButton.clicked.connect(lambda : createTournament(2, self.tournamentNameLabel.text()))
        self.winnersAddPushButton.clicked.connect(lambda : addWinner(self.tournamentNameLabel.text()))
        self.addParticipantsPushButton.clicked.connect(lambda: addParticipants())
        self.seeTreePushButton.clicked.connect(lambda : seeArbre(self.tournamentNameLabel.text()))
        self.previewPushButton_2.clicked.connect(lambda : seeArbre(self.tournamentNameLabel.text(), 2))
        self.delTournamentPushButton.clicked.connect(lambda : delTournament(self.tournamentNameLabel.text()))
        self.delLastElementPushButton.clicked.connect(lambda: self.participantsListListWidget.takeItem(self.participantsListListWidget.count() - 1))
        self.previewPushButton.clicked.connect(lambda: makePreview(self.participantsListListWidget))
        self.startDateEdit.dateChanged.connect(lambda _: self.endDateEdit.setMinimumDate(self.startDateEdit.date()))
        self.validateTournamentPushButton.clicked.connect(lambda: defineTournament(self.tournamentNameLabel.text())) ##
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
        ## Création d'un lien entre les boutons et leur action (fin) ##
        
        self.tableWidget.setSortingEnabled(True)
        
        # Remplissage des QDateTimeEdit
        self.startDateEdit.setMinimumDate(QDate.currentDate())
        self.endDateEdit.setMinimumDate(QDate.currentDate())
        
        self.onLogin()
        
        ## Définition et configuration de l'ImageViewer (QGraphicsView modifié) (début) ##
        self.iw = imageViewer.ImageViewer()
        self.verticalLayout_7.addWidget(self.iw)
        self.iw.show()
        ## Définition et configuration de l'ImageViewer (QGraphicsView modifié) (fin) ##

        
        self.arbiterNameComboBox.addItems(makeRequest.getListeUser() + makeRequest.getListeAdmin())
        
        self.modifyGroupBox.hide()
        
    def onLogin(self) -> None:
        """
        Procédure qui remplit l'ensemble des labels statiques de l'application et qui dépendent seulement de l'utilisateur
        """
        info = makeRequest.getInfo(self.idOfUser)[0]
        self.mailLabel.setText(self.loginId)
        self.dateLabel.setText(info[5])
        self.ageLabel.setText(str(info[4]))
        self.usernameLabel.setText(self.userName)
        
def tournamentClicked(item: int) -> None:
    """
    Procédure qui s'exécute lorsqu'un élément de la table des tournois est cliqué.
    Si c'est le nom d'un tournoi qui est cliqué, alors la page de la visualisation sera mise en place
    Sinon, un filtre sera appliqué à la table.

    Args:
        item (int): élément de la table des tournois
    """
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
        
def hideTree() -> None:
    """
    Procédure qui gère l'affichage de l'arbre de tournoi en fonction de l'état du bouton pour Montre/cacher
    """
    if(application.hidePushButton.isChecked()):
        application.iw.hide()
        application.hidePushButton.setText("Montrer")
    else:
        application.iw.show()
        application.hidePushButton.setText("Cacher")

def hideModifications(state: bool) -> None:
    """
    Procédure qui chache ou montre le groupBox contenant les widgets permettant de modifier les informations
    du profil.

    Args:
        state (bool): l'état du checkBox
    """
    if(state): application.modifyGroupBox.show()
    else: application.modifyGroupBox.hide()

def browseTournament() -> None:
    """
    Procédure qui bascule sur la page d'exploration des tournois
    """
    application.seeMyTournamentsCheckBox.setChecked(False)
    application.userStackedWidget.setCurrentIndex(0)
    application.mainStackedWidget.setCurrentIndex(0)

def manageMyTournaments() -> None:
    """
    Procédure qui bascule sur la page d'exploration des tournois en cochant le checkBox 'Mes tournois'
    """
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

    else: 
        application.tableWidget.setRowCount(0)
        fillTournamentTable()

def fillTableWidget(elements: list[list[str]]) -> None:
    """
    Procédure qui remplie la table des tournois dans l'application à partir d'une liste de listes de chaînes de caractères
    contenant les informations des tournois

    Args:
        elements (list[list[str]]): la liste contenant l'ensemble des tournois et leurs informations respectives
    """
    for i in range(len(elements)):
        application.tableWidget.insertRow(i)
        for j in range(len(elements[i])):
            if(j == 2 or j == 3) : item = QTableWidgetItem(str(datetime.strptime(elements[i][j], "%d/%m/%Y").date()))
            else: item = QTableWidgetItem(elements[i][j])
            item.setForeground(QBrush(QColor(255, 255, 255)))
            application.tableWidget.setItem(i, j, item)

def filterTablesElements(textList: list[str]) -> None:
    """
    Procédure de filtre pour la table des tournois.
    La table est filtrer en fonction des éléments de la liste 'textList'
    passé en paramètre.

    Args:
        textList (list[str]): éléments que doivent contenir les lignes pour être affichées
    """
    if(textList != []):
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
        application.sortComboBox.setCurrentIndex(7)
    else:
        for i in range(application.tableWidget.rowCount()):
            application.tableWidget.setRowHidden(i, False)
        application.sortComboBox.setCurrentIndex(0)
 
def sortTablesElements(sort: int) -> None:
    """
    Procédure qui tri la table des tournois en fonction d'u type de tri passé
    en paramètre :
    - 1 : Nom des tournois par ordre croissant
    - 2 : Nom des tournois par ordre décroissant
    - 3 : Nom du sport par ordre croissant
    - 4 : Nom du sport par ordre décroissant
    - 5 : Date de début la plus récente
    - 6 : Date de début la plus ancienne

    Args:
        sort (int): le type de tri choisi
    """
    if(sort == 0):
        for i in range(application.tableWidget.rowCount()):
            application.tableWidget.setRowHidden(i, False)
    elif(sort == 1): application.tableWidget.sortItems(0, Qt.AscendingOrder)
    elif(sort == 2): application.tableWidget.sortItems(0, Qt.DescendingOrder)
    elif(sort == 3): application.tableWidget.sortItems(1, Qt.AscendingOrder)
    elif(sort == 4): application.tableWidget.sortItems(1, Qt.DescendingOrder)
    elif(sort == 5): application.tableWidget.sortItems(2, Qt.AscendingOrder)
    elif(sort == 6): application.tableWidget.sortItems(2, Qt.DescendingOrder)

def searchTournament(searchedText: str) -> None:
    """
    Procédure qui tri la table en fonction du contenu de la barre de recherche

    Args:
        searchedText (str): le texte de la barre de recherche
    """
    filterTablesElements(searchedText.split())

def createTournament(mode: int, name: str = None) -> None:
    """
    Procédure qui configure la page de création de tournoi en fonction
    de si l'utilisateur souhaite créer un tournoi ou s'il souhaite en modifier un.
    Pour l'argument 'mode' :
    - 1 : pour la création d'un tournoi
    - 2 : pour la configuration d'un tournoi 

    Args:
        mode (int): le mode dans lequel la page va s'ouvrir
        name (str, optional): le nom du tournoi à configurer. Defaults to None.
    """
    application.arbiterListWidget.clear()
    application.participantsListListWidget_2.clear()

    if(mode == 1):
        application.winnerGroupBox.hide()
        application.delTournamentGroupBox.hide()
        application.startDateEdit.setMinimumDate(QDate.currentDate())
        application.endDateEdit.setMinimumDate(QDate.currentDate())
        application.tournamentNameLineEdit.setText("")
        application.tournamentActivityLineEdit.setText("")
        application.tournamentResumeTextEdit.setText("")
        application.participantsGroupBox.show()
        application.createTournamentLabel.setText("Créer un nouveau tournoi")
        application.userStackedWidget.setCurrentIndex(3)
        application.mainStackedWidget.setCurrentIndex(0)
    elif(mode == 2):
        infoTournoi = makeRequest.getInfoTournois(str(name))[0]
        arb = makeRequest.convertSTRtoLst(infoTournoi[2])
        if (application.userName in arb) or (application.userName == infoTournoi[-1]):
            startDate = infoTournoi[8].split("/")
            endDate = infoTournoi[9].split("/")
            startDate = QDate(int(startDate[2]), int(startDate[1]), int(startDate[0]))
            endDate = QDate(int(endDate[2]), int(endDate[1]), int(endDate[0]))
            application.tournamentNameLineEdit.setText(infoTournoi[1])
            application.tournamentActivityLineEdit.setText(infoTournoi[6])
            application.tournamentResumeTextEdit.setText(infoTournoi[7])
            application.startDateEdit.setMinimumDate(startDate)
            application.endDateEdit.setMinimumDate(endDate)
            application.startDateEdit.setDate(startDate)
            application.endDateEdit.setDate(endDate)
            
            for e in arb:
                application.arbiterListWidget.addItem(e)

            for e in makeRequest.convertSTRtoLst(infoTournoi[3]):
                application.participantsListListWidget_2.addItem(e)
                
            application.winnerGroupBox.show()
            application.delTournamentGroupBox.show()
            application.participantsGroupBox.hide()
            application.createTournamentLabel.setText("Modifier un tournoi")
            application.userStackedWidget.setCurrentIndex(3)
            application.mainStackedWidget.setCurrentIndex(0)
    
        else: message.displayMessageBox(4, "Erreur", "Vous ne pouvez pas configurer ce tournoi car vous n'en pas le créateur ni l'arbitre.")

def seeArbre(name: str, b: int = 0) -> None:
    """
    Procédure qui générère et affiche un arbre de tournoi à partir du nom du tournoi.

    Args:
        name (str): le nom du tournoi dont on veut afficher l'arbre
        b (int, optional): valeur indiquant si l'arbre doit contenir les prochains vainqueurs. Defaults to 0.
    """
    infoTournoi = makeRequest.getInfoTournois(str(name))[0]
    liste = makeRequest.arbreSTRtoLIST(infoTournoi[10])
    participant = liste[0]
    arbre = treeGenerator.createTree(participant)
    if len(liste) != 1:
        i = 1
        while (liste[i] != [""]) and (i < len(liste)):
            arbre = treeGenerator.defineWinners(arbre, liste[i])
            i += 1

        if (application.winnersListListWidget.count() != 0) and (b != 0):
            liste[i] = []
            for j in range(0, application.winnersListListWidget.count()):
                liste[i].append(application.winnersListListWidget.item(j).text())
            arbre = treeGenerator.defineWinners(arbre, liste[i])
    
    treeGenerator.drawBinaryTree(arbre, True)

def addWinner(name: str) -> None:
    """
    Procédure qui ajoute le nom d'un des participants à la liste des vainqueurs du prochain tour.
    Le nom des vainqueurs doivent faire partis de ceux des participants précédent.

    Args:
        name (str): nom du tournoi
    """
    infoTournoi = makeRequest.getInfoTournois(str(name))[0]
    win = application.winnersNameLineEdit.text()
    application.winnersNameLineEdit.setText("")
    if win in infoTournoi[3]:
        application.winnersListListWidget.addItem(win)
    else: message.displayMessageBox(4, "Erreur", "Le nom du vainqueur ne figure pas dans dans la liste des participant")

def delTournament(name: str) -> None:
    """
    Procédure qui supprime un tournoi à partir de son nom.

    Args:
        name (str): nom du tournoi
    """
    if application.delTournamentGroupBox.isChecked():
        infoTournoi = makeRequest.getInfoTournois(str(name))[0]
        makeRequest.deleteDataTournoiArbre(infoTournoi[0])
        browseTournament()
        application.seeMyTournamentsCheckBox.setChecked(True)
        application.seeMyTournamentsCheckBox.setChecked(False)
        application.delTournamentGroupBox.setChecked(False)

    else: message.displayMessageBox(4, "Erreur", "La case supprimer n'est pas coché")

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

def defineTournament(aName = None) -> None:
    """
    Procédure qui récupère les informations du tournoi et les enregistre dans la base de donnée
    """
    name = application.tournamentNameLineEdit.text()
    activity = application.tournamentActivityLineEdit.text()
    description = application.tournamentResumeTextEdit.toPlainText()
    startDate = application.startDateEdit.date().toString('dd/MM/yyyy')
    endDate = application.endDateEdit.date().toString('dd/MM/yyyy')
    participants = [application.participantsListListWidget.item(i).text() for i in range(application.participantsListListWidget.count())]
    participants2 = [application.participantsListListWidget_2.item(i).text() for i in range(application.participantsListListWidget_2.count())]
    arbiters = [application.arbiterListWidget.item(i).text() for i in range(application.arbiterListWidget.count())]
    
    if(application.createTournamentLabel.text() == "Modifier un tournoi"):
        infoTournoi = makeRequest.getInfoTournois(str(aName))[0]
        parti = makeRequest.arbreSTRtoLIST(infoTournoi[3])
        #makeRequest.deleteDataTournoiArbre(infoTournoi[0])
        
        
        if (name == "") or (activity == "") or (description == "") or (len(arbiters) < 1):
            message.displayMessageBox(4,"Manque information", "Tous les champs doivent être remplis, la création est impossible.")
        else:
            ### il faut ajouter ici une ligne permettant de créer l'arbre + ajouter les vainqueurs  makeRequest.arbreLISTtoSTR(parti)
            makeRequest.createTournoiArbre(name, arbiters,participants , activity, description, startDate, endDate, application.userName) #ajout nom créateur
            message.displayMessageBox(2, "Réussite", "Modification du tournoi réussi")
            fillTableWidget([[name, activity, str(startDate), str(endDate), makeRequest.getInfo(name)[0][1]]])
    else:    
        if (len(participants) < 2):
            message.displayMessageBox(4, "Manque de participants", "Vous avez entré moins de 2 participants à votre tournoi, la création est impossible.")

        elif ((len(participants)%2) != 0):
            message.displayMessageBox(4, "Manque de participants", f"Vous avez entré un nombre impaire de participants ({len(participants)}) à votre tournoi, la création est impossible.")

        else:
            if (name == "") or (activity == "") or (description == "") or (len(arbiters) < 1):
                message.displayMessageBox(4,"Manque information", "Tous les champs doivent être remplis, la création est impossible.")
            else:
                makeRequest.createTournoiArbre(name, arbiters, participants, activity, description, startDate, endDate, application.userName) #ajout nom créateur
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

def addArbiter() -> None:
    """
    Procédure qui ajoute un arbitre à la liste des arbitres du tournoi.
    """
    arbiterName = application.arbiterNameComboBox.currentText()
    if(application.arbiterNameComboBox.findText(arbiterName) != -1):
        application.arbiterListWidget.addItem(arbiterName)
    else:
        message.displayMessageBox(4, "Arbitre inconnu", "L'utilisateur que vous essayez d'ajouter en tant qu'arbitre de votre tournoi "+
                                  "n'existe pas, veuillez en choisir un dans la liste mise à votre disposition.")

def addParticipants():
    """
    Procédure qui ajoute un participant à la liste des participants du tournoi.
    """
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
    """
    Procédure qui crée un fichier PDF contenant les différentes données stockées en lien avec l'utilisateur.
    """
    userName = "Nom d'utilisateur : " + application.usernameLabel.text()
    mail = "Courrier électronique : " + application.loginId
    date = "Date de création du compte : " + application.dateLabel.text()
    age = "Âge : " + application.ageLabel.text() + " ans"
    ip = "Adresse IP : " + application.ipAddress + " (de l'appareil sur lequel le compte a été créé)"
    
    fileName, _ = QFileDialog.getSaveFileName(None,"Enregistrer mes données", "Mes donnees", "PDF Files (*.pdf)")
    
    if(fileName):
        createPDF.genDataPDF([userName, mail, date, age, ip], fileName)
        os.startfile(fileName) 
    else:
        message.displayMessageBox(3, "Enregistrement impossible", "Vos données n'ont pas pu être téléchargées car l'emplacement saisi est invalide ou inexistant.")

def updateProfile(object: str, id: int) -> None:
    """
    Procédure qui met à jour les informations de l'utilisateur.

    Args:
        object (str): l'information à modifier
        id (int): l'identifiant de l'utilisateur
    """
    if object == "age":
        modif = application.changeAgeSpinBox.value()
        if makeRequest.modifyUserData(id, modif, object) == True: application.ageLabel.setText(str(modif))
        else: message.displayMessageBox(4, "Erreur", "La modification n'a pas pu être effectuée")

    elif object == "email":
        modif = application.changeMailLineEdit.text()
        if makeRequest.modifyUserData(id, modif, object) == True: application.mailLabel.setText(modif)
        else: message.displayMessageBox(4, "Erreur", "La modification n'a pas pu être effectuer, essayez un autre mail")

    elif object == "nom":
        modif = application.changeUsernameLineEdit.text()
        if makeRequest.modifyUserData(id, modif, object) == True: application.usernameLabel.setText(modif)
        else: message.displayMessageBox(4, "Erreur", "La modification n'a pas pu être effectuer, essayez un autre nom")

    elif hash.hash(application.currentPasswordLineEdit.text()) == makeRequest.getInfo(id)[0][3] and object == "mdp":
        modif = hash.hash(application.changePasswordLineEdit.text())
        if makeRequest.modifyUserData(id, modif, object) != True: message.displayMessageBox(4, "Erreur", "La modification n'a pas pu être effectuer")

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
        if makeRequest.registerUserData(pseudo, hash.hash(password), email, age, 1, ip) == True:
            message.displayMessageBox(2, "Inscription réussie", "L'inscription est réussie, " +
                                      "vous pouvez dès maintenant donner ces identifiants au nouvel administrateur pour qu'il/elle se connecte via la page de connexion." + 
                                      "Les identifiants de connexion sont : \n- Identifiant : " + email + "\n- Mot de passe : " + password + "(à conserver secret)")
        else:
            message.displayMessageBox(4, "Erreur d'inscription", "L'inscription a échouée, le nom d'utilisateur ou le mail est probablement déjà utilisé.")
    else:
        message.displayMessageBox(4, "Informations mal complétées", "Au moins l'un des trois champs de saisie est vide, veuillez le/les remplir pour valider votre inscription.")

def delUserAdmin() -> None:
    """
    Procédure qui supprime un utilisateur/administrateur.
    """
    table = makeRequest.getTable("User")
    for e in table:
        if(e[1] == application.accountDelComboBox.currentText()): makeRequest.deleteUserData(e[0])

def sureToAddAdmin(state: bool) -> None:
    """
    Procédure qui gère le bouton pour ajouter un administrateur (couleur, fonctionnment)

    Args:
        state (bool): état de la case à cocher
    """
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
    """
    Procédure qui gère le bouton pour supprimer un utilisateur/administrateur (couleur, fonctionnment)

    Args:
        state (bool): état de la case à cocher
    """
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
    
    fillTournamentTable() # Remplissage de la table des tournois
    
    application.sortComboBox.setCurrentIndex(0)
    application.setMinimumSize(QSize(800, 400))
    application.setMaximumSize(QSize(800, 800))
    application.resize(QSize(800, 600))
    
    app.exec_()