import sqlite3 as sql
"""TEMPLATE INSERT TO METHOD
def insert_account_holder(email,username,phone,password):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO account_holder (email,username,phone,password) VALUES (?,?,?,?)", (email,username,phone,password) )
        con.commit()
"""

def delete_account(user):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE user_id = user")
        con.commit()
