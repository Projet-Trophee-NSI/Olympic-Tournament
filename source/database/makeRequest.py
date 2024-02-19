import sqlite3 
import os
from datetime import*

localPathbd = os.path.dirname(os.path.abspath(__file__))

#### Pour faire des test
# con = sqlite3.connect("storage.db")
# cur = con.cursor()
# cur.execute("DROP TABLE tournoie")
# con.commit()
# con.close()

def inscri_donne (u : str,m : str, e : str, d = datetime.today().strftime('%d-%m-%Y')):
    '''
    u est l'identifient, m est le mdp, e est le mail, d est la date de création du compte
    u -> str
    m -> str
    d -> str
    '''
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    a = cur.execute("SELECT user FROM user WHERE user= ? ", (u,))
    a = a.fetchone()
    if a == None :
        val = (None, u, m, e, d)
        cur.execute("INSERT INTO user VALUES(?,?,?,?,?)", val)
        con.commit()
        con.close()
        return True
    else :
        con.commit()
        con.close()
        return False


def connect (m : str, u : str):
    '''
    m est le mdp de l'utilisateur et u sont identifient
    La fonction retourne : acces ou pas/ l'id de l'utilisateur / 1 si admin et 0 si utilisateur
    m -> str
    u -> str
    '''
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    val = (u,)
    a = cur.execute("SELECT mdp FROM user WHERE user= ? ", val)
    a = a.fetchone()
    if a == None:
        return False,
    else :
        if a[0] == m :
            b = cur.execute("SELECT id, admin FROM user WHERE user= ? AND mdp= ?", (u, m))
            b = b.fetchone()
            con.commit()
            con.close() 
            return True, b[0], b[1]

        else :
            con.commit()
            con.close()
            return False,
    

def modife_donne (i : int,v : str,ch : str):
    '''
    modifie les donner choisie:
    i : id utilisateur -> int
    v : nouvelle valeur -> str
    ch : valeur à modifier -> str
    '''
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    val = (v,i)
    if ch=="mdp":
        cur.execute("UPDATE user SET mdp=? WHERE id= ?", val)
    elif ch=="mail":
        cur.execute("UPDATE user SET user=? WHERE id= ?", val)
    elif ch=="pts":
        cur.execute("UPDATE user SET res_pari=? WHERE id= ?", val)
    con.commit()
    con.close()

def suprime_donne(i:int):
    """
    Supprime un utilisateur de la table user
    i -> int
    """
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    val = (i,)
    cur.execute("DELETE FROM user WHERE id=?", val)
    con.commit()
    con.close()

def cree_tournoie(u,n,p,np,nt):
    '''

    '''
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    a = cur.execute("SELECT user FROM user WHERE user= ? ", (u,))
    a = a.fetchone()
    if a == None :
        val = (None,n,p,np,nt)
        cur.execute("INSERT INTO user VALUES(?,?,?,?,?)", val)
        con.commit()
        con.close()
        return True
    else :
        con.commit()
        con.close()
        return False

def convertSTRtoLst(ch):
    listeFinal=[]
    tempo=''
    for e in ch:
        if e=='[':
            newListe=[]
        elif e==']':
            newListe.append(tempo)
            listeFinal.append(newListe)
            tempo=''
        elif e=='/':
            newListe.append(tempo)
            tempo=''
        else:
            tempo+=e
    return listeFinal

## "[a/b/c/d]"
## [[a,b,c,d,m],[],[],[]]

def convertLsttoSTR(liste):
    pass

#### Fonctions d'aide à la comprehension
def affichTableUser():
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM user")
    res = cur.fetchall()
    con.commit()
    con.close()
    for e in res:
        print(e)

def affichTableTournoi():
    con = sqlite3.connect(localPathbd + "/storage.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM tournoie")
    res = cur.fetchall()
    con.commit()
    con.close()
    for e in res:
        print(e)

affichTableUser()
