import sqlite3 as sql
from datetime import datetime, date

###################INSERT INTO DATABASE###################################
##########################################################################
def insert_restaurant(res_id,name, address, city, state, postal, phone):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO restaurant (res_id,name,address, city, state, postal, phone) VALUES(?,?,?,?,?,?,?)",
                     (res_id, name,address,phone,postal) )
        con.commit()

def insert_employees(emp_id,emp_fname, emp_lname, address, city, state, postal, apt, phone, ssn, birthdate,salary,date_hired):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO employees (emp_id,emp_fname,emp_lname,address,city, state, postal, apt, phone, ssn, birthdate, salary, date_hired) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (emp_id, emp_fname, emp_lname, address, city, state, postal, apt, phone, ssn, birthdate, salary, date_hired) )
        con.commit()

def insert_users(user_id,f_name, l_name, password, address, city, state, postal, apt, phone, acc_funds=100):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        memb_since = datetime.now()
        cur.execute("INSERT INTO users (user_id,f_name, l_name,password,address, city,state, apt, postal,phone,memb_since,acc_funds) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (user_id, f_name, l_name, password, address, city, state, postal, apt, phone, memb_since, acc_funds) )
        con.commit()

#INSERT MORE MONEY INTO ACCOUNT
def insert_funds(user_id,new_funds):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE user set acc_funds = acc_funds + '%s' WHERE user_id = '%s'" %new_funds %user_id)
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
        cur.execute("INSERT INTO orders (order_id,user_id, chef_id, menu_id,menuItem,price, rating) VALUES(?,?,?,?,?,?)",
                    (order_id,user_id, chef_id, menu_id,menuItem,price) )
        con.commit()

def insert_chefs(chef_id,emp_id,menu_name,chef_rating):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO chefs(chef_id, emp_id,menu_name, chef_rating) VALUES (?,?,?,?)", (chef_id,emp_id, menu_name, chef_rating) )
        con.commit()

def insert_deliveryinfo(order_id,emp_id, user_id, status, cust_warning):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO deliveryinfo (order_id,emp_id, user_id, status, cust_warning) VALUES (?,?,?,?,?)",
                    (order_id, emp_id, user_id, status, cust_warning) )
        con.commit()

def insert_menu(chef_id, menu_id, item_name, price, rating):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO menu (chef_id, menu_id, item_name, price, rating) VALUES (?,?,?,?,?)",
                    (chef_id, menu_id, item_name, price, rating))
        con.commit()

################## END OF INSERT INTO DATABASE ###################################
##################################################################################
################## SELECT FROM DATABASE###########################################

################## EMPLOYEE SELECT FUNCTIONS######################################

#GENERAL EMPLOYEE INFO
def select_employee_info(emp_id):
    with sql.connect("losquatroamigos.db") as con:
        cur= con.cursor()
        result = cur.execute("SELECT * FROM Employees where emp_id = '%s';" % emp_id).fetchall()
    return result


################# USER SELECT FUNCTIONS#########################################

#GENERAL USER INFO
def select_user_info(user_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM user WHERE user_id = '%s'" %user_id).fetchall()
    return result

# USERS CAN DELETE THEIR ACCOUNT IF THEY WISH TO DO SO. (MANAGERS MAY ALSO USE THIS TO REMOVE USER FROM WEBSITE)
def delete_account(user_id):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE user_id = '%s'" % user_id)
        con.commit()

#TOP FIVE RATED FOODS OF USER
def select_top_user_rated(user_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        result = cur.execute(
            "SELECT menu_item,rating FROM ratings WHERE user_id = '%s' ORDER BY rate DESC LIMIT 5" % user_id).fetchall()
    return result

#VISITORS TOP 5 RATED FOOD (GET THIS FROM ALL RATED FOOD)
def select_top5_rated():
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        result = cur.execute ("SELECT menu_item, rating FROM ratings ORDER BY rate DESC LIMIT 5 ")
    return result


#COMPLAINTS - Will be neccessary for managers to review
def select_complaints(user_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT complaint, date_posted FROM complaints WHERE user_id = '%s'" %user_id).fetchall()
    return result

#COMPLIMENTS -Will be neccessary for managers to review
def select_compliments(user_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT compliment, date_posted FROM compliments WHERE user_id = '%s'" %user_id).fetchall()
    return result

############### END OF USER SELECT FUNCTIONS#######################################
###################################################################################

############### START DELIVERY INFORMATION#########################################

#We will want to display address/location of person and their name + phone on the delivery order page.
#This function will display all pending delivery orders (where column 'status' is set to '0').

#commented this out because its giving errors

# def select_delivery_info():
#     with sql.connect("losquatroamigos.db") as con:
#         cur = con.cursor()
#         result = cur.execute("SELECT users.f_name, users.address, users.city, users.postal, users.phone FROM users "
#                              "INNER JOIN deliveryinfo ON users.user_id = deliveryinfo.user_id where status in"
#                              "(SELECT status FROM deliveryinfo WHERE status = 0) ").fetchall()
#     return result
#
# #IF we want to view completed deliveres.
# def select_completed_delivery():
#     with sql.connect("losquatroamigos.db") as con:
#         cur = con.cursor()
#         result = cur.execute("SELECT users.f_name, users.address, users.city, users.postal, users.phone FROM users "
#                              "INNER JOIN deliveryinfo ON users.user_id = deliveryinfo.user_id where status in"
#                              "(SELECT status FROM deliveryinfo WHERE status = 1) ").fetchall()
#     return result

def update_delivery_stat(order_id):
   with sql.connect("losquatroamigos.db") as con:
       cur = con.cursor()
       cur.execute("UPDATE deliveryinfo set status = 1 where order_id = '%s'" %order_id)
       con.commit()


#TESTING SOME INSERT FUNCTIONS
#insert_restaurant("1","Los Quatro Amigos", "160 Convent Ave","3123456543", "11365")
#inserting to restaurant works
###############################
fname = "Lenny"
lname = "Gonzalez"
address = "160 Convent Ave"
user_id = "Lenny"
city = "Harlem"
phone = "1234567899"
postal = "11365"
ssn = "123456789"
birthday = "01-01-2017"
salary = "20.25"
date_hired = datetime.now()
emp_id = "C4"
#KEEP COMMENTED.
#insert_employees(emp_id,fname,lname,address,phone,city,ssn,birthday,salary,date_hired)
#print(select_employee_info(emp_id))
#insert_deliveryinfo("1",emp_id, user_id, "0","")

# print(select_delivery_info())
#insert_employees("C0003","Lenny","Gonzalez","160 Convent Ave","1234567899","Harlem","123456789","01-01-2017",)
#inserting to employees works, just need to figure out auto emp_id creation. or have a counter in views.py and concatonate the first letter with counter. e.g C + counter, counter = 1
#insert_users(user_id,fname,lname,"poop","e.simkhayev@gmail.com",address,city,postal,phone,birthday,salary)
