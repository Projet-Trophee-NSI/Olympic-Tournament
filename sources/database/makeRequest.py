### Importation ###
import sqlite3 
import os
import datetime as dat
import math as mat

localPathbd = os.path.dirname(os.path.abspath(__file__))


### Fonctions générales ###
def getTable(name: str) -> list[tuple]:
    """
    Fonction qui permet de récuperer tous les attributs de la table dont le nom
    est passé en paramètre par l'argument 'name'

    Args:
        name (str): nom de la table

    Raises:
        TypeError: vérifie le type de l'argument 'name'
        ValueError: vérifie l'existence de la table

    Returns:
        list[tuple]: le contenu de la table choisie
    """
    if type(name) != str: raise TypeError(f"name must be str not {type(name)}")
    res = False
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    try: cur.execute("SELECT * FROM " + name)
    except: 
        raise ValueError("La table " + name + " n'existe pas")
    else:
        res = cur.fetchall()
        con.commit()
        con.close()
    return res


### Fonctions pour la table User ###
def registerUserData (name: str, password: str, email: str, age: int, admin: int, ip: str, date: str = dat.datetime.today().strftime('%d-%m-%Y')) -> bool:
    """
    Fonction qui inscrit un nouvel utilisateur/administrateur dans la table User

    Args:
        name (str): nom de l'utilisateur
        password (str): mot de passe
        email (str): adresse email
        age (int): age de l'utilisateur
        admin (int): 0/1 pour savoir si la personne est admin
        ip (str): adresse ip de l'utilisateur
        date (str, optional): date de création du compte. Defaults to dat.datetime.today().strftime('%d-%m-%Y').

    Returns:
        bool: état de la réussite de l'inscription (True/False)
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    a = cur.execute("SELECT * FROM User WHERE nom= ? ", (name,))
    a = a.fetchone()
    if a == None :
        val = (findMinimalIdUser(),name, email, password, age, date, admin, ip)
        cur.execute("INSERT INTO user VALUES(?,?,?,?,?,?,?,?)", val)
        con.commit()
        con.close()
        return True
    else :
        con.commit()
        con.close()
        return False

def connect(email: str, password: str) -> tuple[bool, int, int]:
    """
    Fonction qui permet de donner l'accès à l'utilisateur à l'application

    Args:
        email (str): l'adresse mail de l'utilisateur
        password (str): mot de passe de l'utilisateur

    Returns:
        tuple[bool, int, int]: accès ou pas (True/False) / l'id de l'utilisateur / 1 si admin et 0 si utilisateur
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    a = cur.execute("SELECT mdp FROM User WHERE email= ? ", (email,))
    a = a.fetchone()
    if a == None:
        return False,
    else :
        if a[0] == password :
            b = cur.execute("SELECT id, admin FROM User WHERE email= ? AND mdp= ?", (email,password))
            b = b.fetchone()
            con.commit()
            con.close() 
            return True, b[0], b[1]
        else :
            con.commit()
            con.close()
            return False,
    
def modifyUserData(id: int, column: str, newValue: str) -> bool:
    """
    Fonction qui modifie la donnée choisie dans la table User

    Args:
        id (int): identifiant de l'utilisateur
        column (str): colonne où se situe la valeur à modifier
        newValue (str): nouvelle valeur

    Returns:
        bool: True si la modification a été faîte
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    val = (newValue,id)
    if column=="mdp":
        cur.execute("UPDATE User SET mdp=? WHERE id= ?", val)
        con.commit()
        con.close()
        return True
    elif column=="email":
        cur.execute("UPDATE User SET email=? WHERE id= ?", val)
        con.commit()
        con.close()
        return True
    elif column=="age":
        cur.execute("UPDATE User SET age=? WHERE id= ?", val)
        con.commit()
        con.close()
        return True
    elif column=="nom":
        lstNom=cur.execute("SELECT nom FROM User")
        lstNom = lstNom.fetchall()
        if not(newValue in lstNom):
            cur.execute("UPDATE User SET nom=? WHERE id=?",val)
            con.commit()
            con.close()
            return True
        return False
    con.commit()
    con.close()
    return False

def deleteUserData(id: int) -> None:
    """
    Procédure qui supprime un utilisateur de la table user

    Args:
        id (int): identifiant de l'utilisateur
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    cur.execute("DELETE FROM User WHERE id=?", (id,))
    con.commit()
    con.close()

def findMinimalIdUser() -> int:
    """
    Fonction qui renvoie l'id minimal disponible pour la table User

    Returns:
        int: l'id minimal disponible dans la table User
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    lstId=cur.execute("SELECT id FROM User")
    lstId=lstId.fetchall()
    lstId=sorted([row[0] for row in lstId])
    con.commit()
    con.close()
    if lstId==None:
        return 1
    for i in range(len(lstId)-1):
        if lstId[i]+1!=lstId[i+1]:
            return i+2
    return len(lstId)+1

def getInfo(id: int) -> tuple:
    """
    Fonction qui renvoie toutes les informations de l'id donné dans la table User

    Args:
        id (int): id de l'utilisateur

    Returns:
        tuple: l'enregistrement correspondant à l'id de l'utilisateur
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM User WHERE id = ?", (id,))
    inf = cur.fetchall()
    con.commit()
    con.close()
    return inf

def getInfoPrecis(id: int, info: str) -> int|float|str:
    """
    Fonction qui renvie l'information demandée en lien avec l'id donné

    Args:
        id (int): id du compte
        info (str): colone demandée

    Returns:
        int|float|str: la valeur souhaitée
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    cur.execute("SELECT " + info + " FROM User WHERE id = ?", (id,))
    inf = cur.fetchall()
    con.commit()
    con.close()
    return inf[0][0]

def getListeAdmin() -> list[str]:
    """
    Fonction qui renvoie la liste des noms des admins

    Returns:
        list[str]: la liste des noms des admins
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    cur.execute("SELECT nom FROM User WHERE admin = 1")
    inf = cur.fetchall()
    con.commit()
    con.close()
    return [e[0] for e in inf]

def getListeUser() -> list[str]:
    """
    Fonction qui renvoie la liste des noms des utilisateurs

    Returns:
        list[str]: la liste des noms des utilisateurs
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    cur.execute("SELECT nom FROM User WHERE admin = 0")
    inf = cur.fetchall()
    con.commit()
    con.close()
    return [e[0] for e in inf]


### Fonctions pour la table TrournoiArbre ###

## "[a/b/c/d][][][]"
## [[a,b,c,d,m],[],[],[]]
    
def createTournoiArbre(name: str, listIdArbitre: list[int], listParticipants: list[str], activity: str, despcritpion: str , start: str, end: str, createur: str) -> bool:
    """
    Fonction qui crée un nouveau tournoi et renvoie l'état de réussite de la création

    Args:
        name (str): nom du tournoi
        listIdArbitre (list[int]): liste des identifiants des arbitres
        listParticipants (list[str]): liste des participants du tounroi
        activity (str): activité du tournoi
        despcritpion (str): description du tournoi
        start (str): date de début du tournoi
        end (str): date de fin du trounoi
        createur (str): nom du créateur du tournoi

    Returns:
        bool: True si la création a réussi, False sinon
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    a = cur.execute("SELECT nom FROM TournoiArbre WHERE nom= ? ", (name,))
    a = a.fetchone()
    nombreTour = nombersOfTurns(listParticipants)
    if a == None :
        val = (findMinimalIdTournoiArbre(),name,convertLsttoSTR(listIdArbitre),convertLsttoSTR(listParticipants),nombreTour ,len(listParticipants),activity,despcritpion,start,end,arbreLISTtoSTR(createTree(listParticipants,nombreTour)),createur)
        cur.execute("INSERT INTO TournoiArbre VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", val)
        con.commit()
        con.close()
        return True
    else :
        con.commit()
        con.close()
        return False

def convertSTRtoLst(string: str)->list[list[str]]:
    """
    Fonction qui convertie une chaîne de caractères en liste de liste

    Args:
        string (str): chaîne de caractère

    Returns:
        list[list[str]]: liste de liste renvoyée
    """
    tempo=''
    for e in string:
        if e=='[':
            newListe=[]
        elif e==']':
            newListe.append(tempo)
            tempo=''
        elif e=='/':
            newListe.append(tempo)
            tempo=''
        else:
            tempo+=e
    return newListe

def convertLsttoSTR(liste: list)->str:
    """
    Fonction qui convertie une liste en chaîne de caractère

    Args:
        liste (list): liste de liste

    Returns:
        str: chaîne de caractère renvoyée
    """
    chFinale="["
    for j in range(len(liste)):
        chFinale+=str(liste[j])
        if j != len(liste)-1:
            chFinale+="/"
    chFinale+="]"
    return chFinale

def arbreSTRtoLIST(arbreStr: str) -> list:
    """
    Fonction qui convertie un arbre sous la forme d'une chaîne de caractère en liste de listes

    Args:
        arbreStr (str): arbre sous la forme d'une chaîne de caractère

    Returns:
        list: arbre sous la forme d'une liste de listes
    """
    arbreList=[]
    tempo=""
    i=0
    while i<len(arbreStr):
        tempo+=arbreStr[i]
        if arbreStr[i]=="]":
            if tempo != "[]":
                arbreList.append(convertSTRtoLst(tempo))
            else:
                arbreList.append([])
            tempo=""
        i+=1
    return arbreList

def arbreLISTtoSTR(arbreLst: list) -> str:
    """
    Fonction qui convertie un arbre sous la forme d'une liste de listes en chaîne de caractère

    Args:
        arbreLst (list): arbre sous la forme d'une liste de listes

    Returns:
        str: arbre sous la forme d'une chaîne de caractère
    """
    arbreStr=""
    for e in arbreLst:
        arbreStr+=convertLsttoSTR(e)
    return arbreStr

def modifyDataTournoiArbre(id: int, column: str, value: str) -> bool:
    """
    Fonction qui modifie la donnée choisie dans la table TournoiArbre

    Args:
        id (int): identifiant du tournoi
        column (str): colonne à modifier
        valeur (str): nouvelle valeur

    Returns:
        bool: True si la modification a été faîte
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    if column=="arbitre":
        lstArbitre=convertSTRtoLst(cur.execute("SELECT arbitres FROM TournoieArbre"))
        if not(value in lstArbitre):
            value=convertLsttoSTR(lstArbitre.append(value))
            val=(value,id)
            cur.execute("UPDATE TournoiArbre SET arbitres=? WHERE id= ?", val)
        con.commit()
        con.close()
        return True
    elif column=="arbre":
        value=arbreLISTtoSTR(value)
        val=(value,id)
        cur.execute("UPDATE TournoiArbre SET arbre=? WHERE id= ?", val)
        con.commit()
        con.close()
        return True
    elif column=="nom":
        val=(value,id)
        cur.execute("UPDATE TournoiArbre SET nom=? WHERE id= ?", val)
        con.commit()
        con.close()
        return True
    elif column=="description":
        val=(value,id)
        cur.execute("UPDATE TournoiArbre SET description=? WHERE id=?",val)
        con.commit()
        con.close()
        return True
    con.commit()
    con.close()
    return False

def deleteDataTournoiArbre(id: int) -> None:
    """
    Procédure qui supprime un tournoi de la table TournoiArbre.

    Args:
        id (int): identifiant du tournoi
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    cur.execute("DELETE FROM TournoiArbre WHERE id=?", (id,))
    con.commit()
    con.close()

def nombersOfTurns(participantsList: list[int]) -> int:
    """
    Fonction qui renvoie le nombre de tours nécessaires pour un tournoi.

    Args:
        listeParticipant (list[int]): la liste des participants

    Returns:
        int: le nombre de tours
    """
    taille=len(participantsList)
    log = mat.log2(taille)
    if log==int(mat.log2(taille)):
        return int(mat.log2(taille))+1
    return int(mat.log2(taille))+2

def createTree(participantsList: list[int], nb_turns: int) -> list[list]:
    """
    Fonction qui cree l'arbre de tournoi sous la forme d'une liste de liste

    Args:
        participantsList (list[int]): la liste des participants
        nb_turns (int): le nombre de tours du tournoi

    Returns:
        list[list]: arbre de tournoi sous la forme d'une liste de liste
    """
    listeFinals=[[] for i in range(nb_turns)]
    listeFinals[0]=participantsList
    return listeFinals

def findMinimalIdTournoiArbre() -> int:
    """
    Fonction qui renvoie l'id minimal disponible pour la table TournoiArbre

    Returns:
        int: l'id minimal disponible dans la table TournoiArbre
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    lstId=cur.execute("SELECT id FROM TournoiArbre")
    lstId=lstId.fetchall()
    lstId=sorted([row[0] for row in lstId])
    con.commit()
    con.close()
    if lstId==None:
        return 1
    for i in range(len(lstId)-1):
        if lstId[i]+1!=lstId[i+1]:
            return i+2
    return len(lstId)+1

def getInfoTournois(name: str) -> tuple:
    """
    Fonction qui renvoie toutes les informations du nom donné dans la table Tournoi

    Args:
        name (str): nom du tournoi

    Returns:
        tuple: l'enregistrement correspondant au nom du tournoi
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM tournoiArbre WHERE nom=?", (name,))
    res = cur.fetchall()
    con.commit()
    con.close()
    return res