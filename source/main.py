import os
import subprocess

localPath = os.path.dirname(os.path.abspath(__file__))
if(os.path.isfile(localPath + "\\database\\storage.db") and os.path.isfile(localPath + "\\login\\connectApp.py")):
    subprocess.call(["python", localPath + "\\login\\connectApp.py"])
else:
    print("ERREUR : fichiers manquants\nRequis :\n- 'database\\storage.db'\n- 'login\\connectApp.py'")