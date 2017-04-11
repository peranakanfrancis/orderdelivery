import sqlite3 as sql
from datetime import datetime, date


def insert_restaurant(res_id,name, address, phone, postal):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO restaurant (res_id,name,address,phone,postal) VALUES(?,?,?,?,?)",
                     (res_id, name,address,phone,postal) )
        con.commit()

def insert_employees(emp_id,emp_fname, emp_lname, address, city, phone, ssn, birthdate,salary,date_hired):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO employees (emp_id,emp_fname,emp_lname,address,city, phone, ssn, birthdate, salary, date_hired) VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (emp_id, emp_fname, emp_lname, address, city, phone, ssn, birthdate, salary, date_hired) )
        con.commit()

def insert_users(user_id, user_fname, user_lname, password, email, address, postal, phone, memb_since, acc_funds):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO users (user_id,user_fname,user_lname,password,email,address,postal,phone,memb_since,acc_funds) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (user_id, user_fname, user_lname, password, email, address, postal, phone, memb_since, acc_funds) )
        con.commit()

def insert_ratings(user_id, menu_id, menu_item, rating):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execure("INSERT INTO ratings(user_id, menu_id, rating) VALUES(?,?,?)", (user_id, menu_id, menu_item, rating))
        con.commit()

def insert_complaints(user_id, emp_id, date_posted, complaint):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO complaints (user_id, emp_id, date_posted complaint) VALUES(?,?,?)", (user_id, emp_id, date_posted, complaint) )
        con.commit()

def insert_compliments(user_id,emp_id, date_posted, compliment):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO compliments (user_id, emp_id, date_posted, compliment) VALUES(?,?,?)", (user_id, emp_id, date_posted, compliment) )
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

def insert_funds(user_id,acc_funds):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE user set acc_funds ='%s' WHERE user_id = '%s'" %acc_funds %user_id)

def select_employee_info(emp_id):
    with sql.connect("losquatroamigos.db") as con:
        cur= con.cursor()
        result = cur.execute("SELECT * FROM Employees where emp_id = '%s';" % emp_id).fetchall()
    return result

def select_user_info(user_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM user WHERE user_id = '%s'" %user_id).fetchall()
    return result

#get users top 5 rated foods.
def select_top5_rated(user_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT menu_item,rating FROM ratings WHERE user_id = '%s' ORDER BY rate DESC LIMIT 5" %user_id).fetchall()
    return result

#retrieve complaints
def select_complaints(user_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT complaint, date_posted FROM complaints WHERE user_id = '%s'" %user_id).fetchall()
    return result

#retrive compliments
def select_compliments(user_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT compliment, date_posted FROM compliments WHERE user_id = '%s'" %user_id).fetchall()
    return result




#TESTING SOME INSERT FUNCTIONS
#insert_restaurant("1","Los Quatro Amigos", "160 Convent Ave","3123456543", "11365")
#inserting to restaurant works
###############################
fname = "Lenny"
lname = "Gonzalez"
address = "160 Convent Ave"

city = "Harlem"
phone = "1234567899"
ssn = "123456789"
birthday = "01-01-2017"
salary = "20.25"
date_hired = datetime.now()
emp_id = "C4"
#KEEP COMMENTED.
#insert_employees("C4",fname,lname,address,phone,city,ssn,birthday,salary,date_hired)
print(select_employee_info(emp_id))
#insert_employees("C0003","Lenny","Gonzalez","160 Convent Ave","1234567899","Harlem","123456789","01-01-2017",)
#inserting to employees works, just need to figure out auto emp_id creation. or have a counter in views.py and concatonate the first letter with counter. e.g C + counter, counter = 1