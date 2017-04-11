import sqlite3 as sql
"""TEMPLATE INSERT TO METHOD
def insert_account_holder(email,username,phone,password):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO account_holder (email,username,phone,password) VALUES (?,?,?,?)", (email,username,phone,password) )
        con.commit()
"""


def insert_restaurant(res_id,name, address, phone, postal):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execture("INSERT INTO restaurant (res_id,name,address,phone,postal) VALUES(?,?,?,?,?)",
                     (res_id, name,address,phone,postal) )
        con.commit()

def insert_employees(emp_id,emp_fname, emp_lname, address, phone, city, ssn, birthdate,date_hired, salary):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO employees (emp_id,emp_fname,emp_lname,address,phone,city,ssn,birthdate,date_hired,salary) VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (emp_id, emp_fname, emp_lname, address, phone, city, ssn, birthdate, date_hired, salary) )
        con.commit()

def insert_users(user_id,user_fname,user_lname,address,postal,phone,memb_since,acc_funds):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO users (user_id,user_fname,user_lname,address,postal,phone,memb_since,acc_funds) VALUES (?,?,?,?,?,?,?,?,?)",
                    (user_id,user_fname,user_lname,address,postal,phone,memb_since,acc_funds) )
        con.commit()

def insert_ratings(user_id, menu_id, menu_item, rating):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execure("INSERT INTO ratings(user_id, menu_id, rating) VALUES(?,?,?)", (user_id, menu_id, menu_item, rating))
        con.commit()

def insert_complaints(user_id, emp_id, complaint):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO complaints (user_id, emp_id, complaint) VALUES(?,?,?)", (user_id, emp_id, complaint) )
        con.commit()

def insert_compliments(user_id,emp_id,compliment):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO compliments (user_id, emp_id,compliment) VALUES(?,?,?)", (user_id, emp_id, compliment) )
        con.commit()

def insert_orders(order_id,user_id, chef_id, menu_id,menuItem,price):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO orders (order_id,user_id, chef_id, menu_id,menuItem,price, rating) VALUES(?,?,?,?,?,?",
                    (order_id,user_id, chef_id, menu_id,menuItem,price) )
        con.commit()

def insert_chefs(chef_id,emp_id,chef_rating):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO chefs(chef_id, emp_id, chef_rating) VALUES (?,?,?)", (chef_id,emp_id,chef_rating) )
        con.commit()

def insert_deliveryinfo(emp_id, user_id, user_name,address,city,postal, cust_warning):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO deliveryinfo (emp_id, user_id, user_name,address,city,postal, cust_warning) VALUES (?,?,?,?,?,?,?)",
                    (emp_id, user_id, user_name,address,city,postal, cust_warning) )
        con.commit()

def insert_menu(chef_id, menu_id, item_name, price, rating):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO menu (chef_id, menu_id, item_name, price, rating) VALUES (?,?,?,?,?)",
                    (chef_id, menu_id, item_name, price, rating))
        con.commit()

