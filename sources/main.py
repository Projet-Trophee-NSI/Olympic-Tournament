### Importation ###
import os
import subprocess

localPath = os.path.dirname(os.path.abspath(__file__)) # Chemin absolu local

## Définition des booléens vérifiant la présence des fichiers sources (début) ##
isStorageFile = os.path.isfile(localPath + "\\database\\storage.db")
isConnectAppFile = os.path.isfile(localPath + "\\login\\connectApp.py")
isApplicationFile = os.path.isfile(localPath + "\\application\\application.py")
isMakeRequestFile = os.path.isfile(localPath + "\\database\\makeRequest.py")
isCreatePDFFile = os.path.isfile(localPath + "\\tools\\createPDF.py")
isDisplayMessageBoxFile = os.path.isfile(localPath + "\\tools\\displayMessageBox.py")
isGetIPFile = os.path.isfile(localPath + "\\tools\\getIP.py")
isHashFile = os.path.isfile(localPath + "\\tools\\hash.py")
isImageViewerFile = os.path.isfile(localPath + "\\tools\\imageViewer.py")
isTreeGeneratorFile = os.path.isfile(localPath + "\\tools\\treeGenerator.py")
## Définition des booléens vérifiant la présence des fichiers sources (fin) ##

isThereAllFiles = not False in [isStorageFile, isConnectAppFile, isApplicationFile, isMakeRequestFile, isCreatePDFFile, 
                                isDisplayMessageBoxFile, isGetIPFile, isHashFile, isImageViewerFile, isTreeGeneratorFile] # Booléen indiquant s'il manque des fichiers

if(isThereAllFiles):
    subprocess.call(["python", localPath + "\\login\\connectApp.py"]) # Exécution de la fenêtre de connexion
else:
    print("ERREUR : fichier(s) manquant(s)\nRequis :\n- 'database\\storage.db'\n- 'database\\makeRequest.py'\n- 'login\\connectApp.py'" +
          "\n- 'application\\application.py'\n- 'tools\\createPDF.py'\n- 'tools\\displayMessageBox.py'\n- 'tools\\getIP.py'" + 
          "\n- 'tools\\imageViewer.py'\n- 'tools\\treeGenerator.py'")