import sqlite3 as sql
"""TEMPLATE INSERT TO METHOD
def insert_account_holder(email,username,phone,password):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO account_holder (email,username,phone,password) VALUES (?,?,?,?)", (email,username,phone,password) )
        con.commit()
"""

def add_money(user, amount_to_add):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET acc_funds = acc_funds + amount_to_add WHERE user_id = user")
        con.commit()
