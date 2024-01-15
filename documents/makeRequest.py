import sqlite3 


'''
cur.execute ("CREATE TABLE user(user VARCHAR, mdp VARCHAR, date_cr DATE, res_pari INT)")
'''


def insert_donne (a : str,b : str,c : str,d : int):
    '''a est l'identifient, b est le mdp, c est la date et d est sont nb de point/ argent on vera'''
    con = sqlite3.connect("storage.db")
    cur = con.cursor()
    val = (a, b, c, d)
    cur.execute ("INSERT INTO user VALUES(?,?,?,?)", val)
    con.commit()
    con.close()


def connect (m : str, u : str):
    '''m est le mdp de l'utilisateur et u sont identifient'''
    con = sqlite3.connect("storage.db")
    cur = con.cursor()
    val = (u,)
    a = cur.execute ("SELECT mdp FROM user WHERE user= ? ", val)
    a = a.fetchone()
    con.commit()
    con.close()
    if a == None:
        return False
    else :
        if a[0] == m :
            return True
        else :
            return False
    




print (connect ("admin", "Lucas"))
