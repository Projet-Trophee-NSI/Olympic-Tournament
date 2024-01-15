import sqlite3 
'''
con = sqlite3.connect("storage.db")
cur = con.cursor()
cur.execute ("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, user VARCHAR, mdp VARCHAR, date_cr DATE, res_pari INT)")
con.commit()
con.close()
'''

def insert_donne (a : str,b : str,c : str,d : int):
    '''a est l'identifient, b est le mdp, c est la date et d est sont nb de point/ argent on vera'''
    con = sqlite3.connect("storage.db")
    cur = con.cursor()
    val = (None, a, b, c, d)
    cur.execute ("INSERT INTO user VALUES(?,?,?,?,?)", val)
    con.commit()
    con.close()


def connect (m : str, u : str):
    '''m est le mdp de l'utilisateur et u sont identifient
    en plus j'ai rajouté une id qui s'auto incrémente comme ça une fois l'utilisateur connecter ou pourra directement 
    récupérer ces info avec l'id que l'on aura stocke quelque part'''
    con = sqlite3.connect("storage.db")
    cur = con.cursor()
    val = (u,)
    a = cur.execute ("SELECT mdp FROM user WHERE user= ? ", val)
    a = a.fetchone()
    if a == None:
        return False
    else :
        if a[0] == m :
            b = cur.execute("SELECT id FROM user WHERE user= ? AND mdp= ?", (u, m,))
            b = b.fetchone()
            con.commit()
            con.close() 
            return True, b

        else :
            con.commit()
            con.close()
            return False
    


a = connect("admin", "Lucas")
print(a)


