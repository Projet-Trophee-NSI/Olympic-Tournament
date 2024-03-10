import sqlite3 
import os
from datetime import *
import math as mat

localPathbd = os.path.dirname(os.path.abspath(__file__))


def getTable(name : str) -> list[tuple]:
    """
    permet de récuperer tous les attribues de la table d'un nom donné
    name : nom de la table -> str
    """
    if type(name) != str: raise TypeError(f"name must be str not {type(name)}")
    res = False
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    try: cur.execute(f"SELECT * FROM {name}")
    except: 
        raise ValueError(f"La table {name} n'existe pas")
    else:
        cur.execute(f"SELECT * FROM {name}")
        res = cur.fetchall()
        con.commit()
        con.close()
    return res


################# FONCTIONS POUR LA TABLE User
def inscri_donne (nom: str, mdp: str, email: str, age: int, admin:int, ip : str, date: str = datetime.today().strftime('%d-%m-%Y')) -> bool:
    '''
    Inscrie une nouvelle personne dans la table User
    nom : nom de l'utilisateur -> str
    mdp : mot de passe -> str
    email : adresse email -> str
    age : age de la personne -> int
    date : date de création du compte -> str
    admin : 0/1 pour savoir si la personne est admin -> int
    ip : adresse ip de l'utilisateur -> str
    '''
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    a = cur.execute("SELECT * FROM User WHERE nom= ? ", (nom,))
    a = a.fetchone()
    if a == None :
        val = (trouver_minimal_id_user(),nom, email, mdp, age, date, admin, ip)
        cur.execute("INSERT INTO user VALUES(?,?,?,?,?,?,?,?)", val)
        con.commit()
        con.close()
        return True
    else :
        con.commit()
        con.close()
        return False

def connect(email : str, mdp : str) -> tuple[bool,int,int]:
    '''
    La fonction retourne : acces ou pas/ l'id de l'utilisateur / 1 si admin et 0 si utilisateur
    mdp : mot de passe -> str
    nom : nom de l'utilisateur-> str
    '''
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    val = (email,)
    a = cur.execute("SELECT mdp FROM User WHERE email= ? ", val)
    a = a.fetchone()
    if a == None:
        return False,
    else :
        if a[0] == mdp :
            b = cur.execute("SELECT id, admin FROM User WHERE email= ? AND mdp= ?", (email,mdp))
            b = b.fetchone()
            con.commit()
            con.close() 
            return True, b[0], b[1]
        else :
            con.commit()
            con.close()
            return False,
    
def modife_donne_user(id : int, valeur: str, colone : str):
    '''
    Modifie les donners choisies:
    id : identifiant de l'utilisateur -> int
    valeur : nouvelle valeur -> str
    colone : colone à modifier -> str
    '''
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    val = (valeur,id)
    if colone=="mdp":
        cur.execute("UPDATE User SET mdp=? WHERE id= ?", val)
        return True
    elif colone=="email":
        cur.execute("UPDATE User SET email=? WHERE id= ?", val)
        return True
    elif colone=="age":
        cur.execute("UPDATE User SET age=? WHERE id= ?", val)
        return True
    elif colone=="nom":
        lstNom=cur.execute("SELECT nom FROM User")
        lstNom = lstNom.fetchall()
        if not(valeur in lstNom):
            cur.execute("UPDATE User SET nom=? id=?",val)
            return True
        return False
    con.commit()
    con.close()

def suprime_donne_user(id:int):
    """
    Supprime un utilisateur de la table user
    id : identifiant de l'utilisateur -> int
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    val = (id,)
    cur.execute("DELETE FROM User WHERE id=?", val)
    con.commit()
    con.close()

def trouver_minimal_id_user():
    """
    Renvoie l'id minimal disponible pour la table User
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    lstId=cur.execute("SELECT id FROM User")
    lstId=lstId.fetchall()
    print(lstId)
    lstId=sorted([row[0] for row in lstId])
    con.commit()
    print(lstId)
    con.close()
    if lstId==None:
        return 1
    for i in range(len(lstId)-1):
        if lstId[i]+1!=lstId[i+1]:
            return i+2
    return len(lstId)+1

def getinfo(id:int) -> tuple:
    """
    Fonction renvoyant toutes les information de l'id donnée
    id : id du compte -> int
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM User WHERE id = ?", (id,))
    inf = cur.fetchall()
    con.commit()
    con.close()
    return inf

def getinfoPrecis(id:int, info:str):
    """
    Fonction renvoyant l'information demander en lien avec l'id donnée
    id : id du compte -> int
    info : colone demander -> str
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    cur.execute("SELECT "+info+" FROM User WHERE id = ?", (id,))
    inf = cur.fetchall()
    con.commit()
    con.close()
    return inf[0][0]

def getListeAdmin():
    """
    Fonction renvoyant la liste des noms des admin
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    cur.execute("SELECT nom FROM User WHERE admin = 1")
    inf = cur.fetchall()
    con.commit()
    con.close()
    return [e[0] for e in inf]

def getListeUser():
    """
    Fonction renvoyant la liste des noms des user
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    cur.execute("SELECT nom FROM User WHERE admin = 0")
    inf = cur.fetchall()
    con.commit()
    con.close()
    return [e[0] for e in inf]


################# FONCTIONS POUR LA TABLE TournoiArbre

## "[a/b/c/d][][][]"
## [[a,b,c,d,m],[],[],[]]
    
def cree_TournoiArbre(nom:str,listeIdArbitre:list[int],listeParticipant:list[str],sport,despcritpion,debut,fin) -> bool:
    '''
    cree un nouveau tournoi et revoie si la création a réussie
    nom : nom du tournoi -> str
    listeIdArbitre : liste des identifiant des arbitres -> list[int]
    listeParticipant : list des participan du tounroie -> list[str]
    sport : sport du tournoie -> str
    description : description du tournoie -> str
    debut : date de début du tournoie -> str
    fin : date de fin du trounoie -> str
    '''
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    a = cur.execute("SELECT nom FROM TournoiArbre WHERE nom= ? ", (nom,))
    a = a.fetchone()
    if a == None :
        val = (trouver_minimal_id_tournoiArbre(),nom,convertLsttoSTR(listeIdArbitre),convertLsttoSTR(listeParticipant),nombreTour(listeParticipant),len(listeParticipant),sport,despcritpion,debut,fin,arbreLISTtoSTR(cree_arbre(listeParticipant,nombreTour(listeParticipant))))
        cur.execute("INSERT INTO TournoiArbre VALUES(?,?,?,?,?,?,?,?,?,?,?)", val)
        con.commit()
        con.close()
        return True
    else :
        con.commit()
        con.close()
        return False

def convertSTRtoLst(ch:str)->list[list[str]]:
    """
    convertie une chaine de charactère en liste de liste
    ch -> str
    """
    tempo=''
    for e in ch:
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

def convertLsttoSTR(liste:list)->str:
    """
    convertie une liste en chaine de charactère
    liste -> list
    """
    chFinale="["
    for j in range(len(liste)):
        chFinale+=str(liste[j])
        if j != len(liste)-1:
            chFinale+="/"
    chFinale+="]"
    return chFinale

def arbreSTRtoLIST(arbreStr):
    arbreList=[]
    tempo=""
    i=0
    while i<len(arbreStr):
        tempo+=arbreStr[i]
        if arbreStr[i]=="]":
            arbreList.append(convertSTRtoLst(tempo))
            tempo=""
        i+=1
    return arbreList

def arbreLISTtoSTR(arbreLst):
    arbreStr=""
    for e in arbreLst:
        arbreStr+=convertLsttoSTR(e)
    return arbreStr

def modife_donne_tournoiArbre(id: int,valeur : str,colone : str):
    '''
    modifie les donner choisie:
    id : identifiant du tournoie -> int
    valeur : nouvelle valeur -> str
    colone : colone à modifier -> str
    '''
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    if colone=="arbitre":
        lstArbitre=convertSTRtoLst(cur.execute("SELECT arbitres FROM TournoieArbre"))
        if not(valeur in lstArbitre):
            valeur=convertLsttoSTR(lstArbitre.append(valeur))
            val=(valeur,id)
            cur.execute("UPDATE TournoiArbre SET arbitres=? WHERE id= ?", val)
        con.commit()
        con.close()
        return True
    elif colone=="arbre":
        valeur=arbreLISTtoSTR(valeur)
        val=(valeur,id)
        cur.execute("UPDATE TournoiArbre SET arbre=? WHERE id= ?", val)
        con.commit()
        con.close()
        return True
    elif colone=="nom":
        val=(valeur,id)
        cur.execute("UPDATE TournoiArbre SET nom=? WHERE id= ?", val)
        con.commit()
        con.close()
        return True
    elif colone=="description":
        val=(valeur,id)
        cur.execute("UPDATE TournoiArbre SET description=? WHERE id=?",val)
        con.commit()
        con.close()
        return True
    con.commit()
    con.close()
    return False

def suprime_donne_tournoiArbre(id:int):
    """
    Supprime un utilisateur de la table user
    id : identifiant -> int
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    val = (id,)
    cur.execute("DELETE FROM TournoiArbre WHERE id=?", val)
    con.commit()
    con.close()

def nombreTour(listeParticipant:list[int])->int:
    """
    renvoie le nombre de tour nessesaire pour le tournoi
    liste_participan -> list
    """
    taille=len(listeParticipant)
    if mat.log2(taille)==int(mat.log2(taille)):
        return int(mat.log2(taille))+1
    return int(mat.log2(taille))+2

def cree_arbre(liste_participant:list[int],nb_tour:int)->list[list]:
    """
    cree l'arbre de tournoi
    liste_participant -> list
    nb_tour -> int
    """
    listeFinals=[[] for i in range(nb_tour)]
    listeFinals[0]=liste_participant
    return listeFinals

def trouver_minimal_id_tournoiArbre()->int:
    """
    Renvoie l'id minimal disponible pour la table TournoiArbre
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    lstId=cur.execute("SELECT id FROM TournoiArbre")
    lstId=lstId.fetchall()
    print(lstId)
    lstId=sorted([row[0] for row in lstId])
    print(lstId)
    con.commit()
    con.close()
    if lstId==None:
        return 1
    for i in range(len(lstId)-1):
        if lstId[i]+1!=lstId[i+1]:
            return i+2
    return len(lstId)+1
