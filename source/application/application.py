from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QListWidget, QLineEdit
from PyQt5.QtGui import QPixmap, QIcon, QColor, QBrush
from PyQt5.QtCore import Qt, QDate
from PyQt5.uic import loadUi
from datetime import datetime
import os
import sys
import ctypes

localPath = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, localPath + "/../tools")

import treeGenerator
import displayMessageBox as message
import imageViewer

class MonApplication(QMainWindow):
    def __init__(self):
        super(MonApplication, self).__init__() #<- comprend pas le super
        
        self.setWindowTitle("Best tournament")
        self.setWindowIcon(QIcon(localPath + "/../ressources/mainLogo.jpg"))
        
        # Créer un widget central
        #self.windowContent = QWidget()
        #self.setCentralWidget(self.windowContent)
        
        # Charger l'interface utilisateur dans le widget central
        loadUi(localPath + "/application.ui", self)
        
        self.actionBrowse.setIcon(QIcon(localPath + "/../ressources/browseIcon.png"))
        self.actionCreate.setIcon(QIcon(localPath + "/../ressources/createIcon.png"))
        self.actionMyTournaments.setIcon(QIcon(localPath + "/../ressources/configureIcon.png"))
        self.actionProfile.setIcon(QIcon(localPath + "/../ressources/profileIcon.png"))
        self.mainIconLabel.setPixmap(QPixmap(localPath + "/../ressources/mainLogo.jpg"))
        
        self.actionBrowse.triggered.connect(browseTournament)
        self.actionCreate.triggered.connect(lambda: createTournament(1))
        self.actionMyTournaments.triggered.connect(manageMyTournaments)
        self.actionProfile.triggered.connect(lambda: self.userStackedWidget.setCurrentIndex(2))
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
        
        sortingItems = ["Aucun", "Noms croissants", "Noms décroissant", "Sports croissants", "Sports décroissants", "Plus récent", "Plus ancien", "Tri personnalisé"]
        self.sortComboBox.addItems(sortingItems)
        
        self.tableWidget.setSortingEnabled(True)
        
        self.startDateEdit.setMinimumDate(QDate.currentDate())
        self.endDateEdit.setMinimumDate(QDate.currentDate())
        
        ## TEMPORAIRE
        self.iw = imageViewer.ImageViewer()
        self.iw.setPhoto(QPixmap(localPath + "/../tools/treePreview.png"))
        self.verticalLayout_7.addWidget(self.iw)
        self.iw.show()
        ## TEMPORAIRE
        
        self.modifyGroupBox.hide()
        
def tournamentClicked(item):
    if(item.column() == 0):
        application.tournamentNameLabel.setText(item.text())
        ## COMPLETER L'ENSEMBLE DES INFORMATIONS DE LA PAGE VISUALISATION AVEC LA BDD ET 'treeGenerator'
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

def manageMyTournaments():
    if(not(application.seeMyTournamentsCheckBox.isChecked())):
        application.seeMyTournamentsCheckBox.setChecked(True)
    application.userStackedWidget.setCurrentIndex(0)
    
def manageMyTournamentsSelect(state: bool) -> None:
    """
    Procédure qui permet l'affichage des tournois dont l'utilisateur est arbitre

    Args:
        state (bool): Etat de la case, si elle est cochée alors on filtre
    """
    if(state):
        pass # Afficher les tournois que l'utilisateur a créé
            
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
        application.participantsGroupBox.show()
        application.createTournamentLabel.setText("Créer un nouveau tournoi")
    elif(mode == 2):
        application.winnerGroupBox.show()
        application.participantsGroupBox.hide()
        application.createTournamentLabel.setText("Modifier un tournoi")
    application.userStackedWidget.setCurrentIndex(3)

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
    A COMPLETER
    """
    name = application.tournamentNameLineEdit.text()
    activity = application.tournamentActivityLineEdit.text()
    description = application.tournamentResumeTextEdit.toPlainText()
    startDate = application.startDateEdit.date().toString('dd/MM/yyyy')
    endDate = application.endDateEdit.date().toString('dd/MM/yyyy')
    partcipants = [application.participantsListListWidget.item(i).text() for i in range(application.participantsListListWidget.count())]
    arbiters = [application.arbiterListWidget.item(i).text() for i in range(application.arbiterListWidget.count())]
    
    ## FAIRE LE LIEN AVEC LA BDD

def fillTournamentTable() -> None:
    """
    Procédure qui rempli le tableau contenant l'ensemble des tournois à partir de la base de données
    A COMPLETER    
    """

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
    current_mode = application.newPasswordLineEdit.echoMode() #recupère le mode d'affichage actuelle  de passwordLineEdit
    new_mode = QLineEdit.Normal if current_mode == QLineEdit.Password else QLineEdit.Password #affecte un mode affichage avec : QLineEdit.Normal : Affiche le texte normalement|QLineEdit.Password : Affiche des caractères de remplacement pour masquer le texte
    application.newPasswordLineEdit.setEchoMode(new_mode) #modifie le mode de l'affichage de passwordLineEdit

if __name__ == '__main__':
    app = QApplication([])
    
    ## Forcer l'icône de la barre des tâche (début) ##
    # Provient de : https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
    myappid = 'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app.setWindowIcon(QIcon(localPath + "/../ressources/mainLogo.ico"))
    ## Forcer l'icône de la barre des tâche (fin) ##
    
    application = MonApplication()
    application.show()
    
    fillTableWidget([["Tournoi 1", "Tennis", "23/02/2024", "25/02/2024", "Antoine"], ["Tournoi 2", "Pétanque", "20/02/2024", "18/04/2024", "Jonathan"]])
    
    application.sortComboBox.setCurrentIndex(0)
    
    app.exec_()