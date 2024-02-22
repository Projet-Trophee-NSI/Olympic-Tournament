from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.uic import loadUi
import os
import ctypes

localPath = os.path.dirname(os.path.abspath(__file__))

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
        
        self.optionsPushButton.clicked.connect(lambda: application.userStackedWidget.setCurrentIndex(2))
        self.backPushButton.clicked.connect(lambda: application.userStackedWidget.setCurrentIndex(0))
        self.hidePushButton.clicked.connect(hideTree)
        self.browserListWidget.itemClicked.connect(tournamentClicked)
        
def tournamentClicked(item):
    application.tournamentNameLabel.setText(item.text())
    application.userStackedWidget.setCurrentIndex(1)
        
def hideTree():
    if(application.hidePushButton.isChecked()):
        application.treeImageLabel.hide()
        application.hidePushButton.setText("Montrer")
    else:
        application.treeImageLabel.show()
        application.hidePushButton.setText("Cacher")
        
    
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
    app.exec_()