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

def insert_employees(emp_id,emp_fname, emp_lname, address, city, state, postal, apt, phone, ssn, birthdate,salary,date_hired, hired=0):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO employees (emp_id,emp_fname,emp_lname,address,city, state, postal, apt, phone, ssn, birthdate, salary, date_hired, hired) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (emp_id, emp_fname, emp_lname, address, city, state, postal, apt, phone, ssn, birthdate, salary, date_hired,hired) )
        con.commit()

def insert_users(user_id,f_name, l_name, password, address, city, state, postal, apt, phone, acc_funds=100,registered=0):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        memb_since = datetime.now()
        cur.execute("INSERT INTO users (user_id,f_name, l_name,password,address, city,state, apt, postal,phone,memb_since,acc_funds,registered) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (user_id, f_name, l_name, password, address, city, state, postal, apt, phone, memb_since, acc_funds,registered))
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
        cur.execute("INSERT INTO ratings(user_id, menu_id, rating) VALUES(?,?,?)", (user_id, menu_id, menu_item, rating))
        con.commit()

def insert_complaints(user_id, emp_id, complaint):
    date = datetime.now()
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO complaints (user_id, emp_id, date_posted, complaint) VALUES(?,?,?,?)", (user_id, emp_id, date, complaint) )
        con.commit()

def insert_compliments(user_id, emp_id, compliment):
    date = datetime.now()
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO compliments (user_id, emp_id, date_posted, compliment) VALUES(?,?,?,?)", (user_id, emp_id, date, compliment) )
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
#SELECT ALL UNREGISTERED USERS
def select_all_unregistered_users():
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM users WHERE registered = 0").fetchall()
    return result

def select_all_registered_users():
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM users").fetchall()
    return result

def select_all_hired_employees():
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM employees WHERE hired = 1").fetchall()
    return result



#GENERAL USER INFO
def select_user_info(user_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT * FROM users WHERE user_id = '%s'" %user_id).fetchall()
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

########## MANAGEMENT FUNCTIONS ##########################

#Accept Registration
def register(user_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET registered=1 WHERE user_id = '%s'" %user_id)
        con.commit()

#hire employee
def hire_employee(emp_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE employees SET hired = 1 where emp_id ='%s'" %emp_id)
        con.commit()

def add_demotions(emp_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.execute()
        cur.execute("UPDATE employees SET demotions = demotions + 1 WHERE emp_id = '%s'" %emp_id)
        con.commit()

def decrease_demotions(emp_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.execute()
        cur.execute("UPDATE employees SET demotions = demotions - 1 WHERE emp_id = '%s'" %emp_id)
        con.commit()

def check_demotions(emp_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.execute()
        result = cur.execute("SELECT demotions FROM employees WHERE emp_id = '%s'" %emp_id).fetchone()
        return result

def fire_employee(emp_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE employees SET hired = 0 where emp_id '%s'" %emp_id)
        con.commit()

#Promoting employee increases their salary by 5 dollars.
def check_compliments(emp_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT count(*) FROM compliments WHERE emp_id = '%s'" %emp_id).fetchall()
        return result

def promote_employee(emp_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE employees SET salary = salary + 5 where emp_id = '%s'" %emp_id)
        con.commit()

#demoting employee
def check_complaints(emp_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        result = cur.execute("SELECT count(*) FROM complaints WHERE emp_id '%s'" %emp_id).fetchall()
        return result

def demote_employee(emp_id):
    with sql.connect("losquatroamgos.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE employees SET salary = salary - 5 WHERE emp_id = '%s'" %emp_id)
        con.commit()



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

#update warnings in users table. Do this by counting the number of true boolean values a user has in the warnings column
# of delivery info table.
def update_warnings(user_id):
    with sql.connect("losquatroamigos.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE users set warnings = (SELECT count(cust_warning) FROM deliveryinfo where user_id = '%s')"
                    %user_id)
        con.commit()


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
