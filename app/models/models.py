import sqlite3 as sql
from datetime import datetime, date


class db_connect:
    def __init__(self):
        #establish connection.
        with sql.self.connect("losquatroamigos.db")as self.self.con:
            self.cur = self.self.con.self.cursor()


    ###################INSERT INTO DATABASE###################################
    ##########################################################################
    def insert_restaurant(self,res_id,name, address, city, state, postal, phone):
        self.cur = self.self.con.self.cursor()
        self.cur.execute("INSERT INTO restaurant (res_id,name,address, city, state, postal, phone) VALUES(?,?,?,?,?,?,?)",
                     (res_id, name,address,phone,postal) )
        self.con.commit()

    def insert_employees(self,emp_id,emp_fname, emp_lname, address, city, state, postal, apt, phone, ssn, birthdate,salary,date_hired, hired=0):
        self.cur = self.self.con.self.cursor()
        self.cur.execute("INSERT INTO employees (emp_id,emp_fname,emp_lname,address,city, state, postal, apt, phone, ssn, birthdate, salary, date_hired, hired) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (emp_id, emp_fname, emp_lname, address, city, state, postal, apt, phone, ssn, birthdate, salary, date_hired,hired) )
        self.con.commit()

    def insert_users(self,user_id,f_name, l_name, password, address, city, state, postal, apt, phone, acc_funds=100,registered=0):
        self.cur = self.self.con.self.cursor()
        memb_since = datetime.now()
        self.cur.execute("INSERT INTO users (user_id,f_name, l_name,password,address, city,state, apt, postal,phone,memb_since,acc_funds,registered) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (user_id, f_name, l_name, password, address, city, state, postal, apt, phone, memb_since, acc_funds,registered))
        self.con.commit()

    #INSERT MORE MONEY INTO ACCOUNT
    def insert_funds(self,user_id,new_funds):
        self.cur = self.con.self.cursor()
        self.cur.execute("UPDATE user set acc_funds = acc_funds + '%s' WHERE user_id = '%s'" %new_funds %user_id)
        self.con.commit()
    
    def insert_ratings(self,user_id, menu_id, menu_item, rating):
        self.cur = self.con.self.cursor()
        self.cur.execute("INSERT INTO ratings(user_id, menu_id, rating) VALUES(?,?,?)", (user_id, menu_id, menu_item, rating))
        self.con.commit()
    
    def insert_complaints(self,user_id, emp_id, complaint):
        date = datetime.now()
        self.cur = self.con.self.cursor()
        self.cur.execute("INSERT INTO complaints (user_id, emp_id, date_posted, complaint) VALUES(?,?,?,?)", (user_id, emp_id, date, complaint) )
        self.con.commit()
    
    def insert_compliments(self,user_id, emp_id, compliment):
        date = datetime.now()
        self.cur = self.con.self.cursor()
        self.cur.execute("INSERT INTO compliments (user_id, emp_id, date_posted, compliment) VALUES(?,?,?,?)", (user_id, emp_id, date, compliment) )
        self.con.commit()
    
    def insert_orders(self,order_id,user_id, chef_id, menu_id,menuItem,price):
        self.cur = self.con.self.cursor()
        self.cur.execute("INSERT INTO orders (order_id,user_id, chef_id, menu_id,menuItem,price, rating) VALUES(?,?,?,?,?,?)",
                    (order_id,user_id, chef_id, menu_id,menuItem,price) )
        self.con.commit()
    
    def insert_chefs(self,chef_id,emp_id,menu_name,chef_rating):
        self.cur = self.con.self.cursor()
        self.cur.execute("INSERT INTO chefs(chef_id, emp_id,menu_name, chef_rating) VALUES (?,?,?,?)", (chef_id,emp_id, menu_name, chef_rating) )
        self.con.commit()
    
    def insert_deliveryinfo(self,order_id,emp_id, user_id, status, cust_warning):
        self.cur = self.con.self.cursor()
        self.cur.execute("INSERT INTO deliveryinfo (order_id,emp_id, user_id, status, cust_warning) VALUES (?,?,?,?,?)",
                        (order_id, emp_id, user_id, status, cust_warning) )
        self.con.commit()
    
    def insert_menu(self,chef_id, menu_id, item_name, price, rating):
        self.cur = self.con.self.cursor()
        self.cur.execute("INSERT INTO menu (chef_id, menu_id, item_name, price, rating) VALUES (?,?,?,?,?)",
                        (chef_id, menu_id, item_name, price, rating))
        self.con.commit()
    
    ################## END OF INSERT INTO DATABASE ###################################
    ##################################################################################

    ################## SELECT FROM DATABASE###########################################

    
    ################## EMPLOYEE SELECT FUNCTIONS######################################
    
    #GENERAL EMPLOYEE INFO
    def select_employee_info(self,emp_id):
        self.cur= self.con.self.cursor()
        result = self.cur.execute("SELECT * FROM Employees where emp_id = '%s';" % emp_id).fetchone()
        return result

    def select_all_hired_employees(self):
        self.cur = self.con.self.cursor()
        result = self.cur.execute("SELECT * FROM employees WHERE hired = 1").fetchall()
        return result

    def select_all_pending_employees(self):
        self.cur = self.con.self.cursor()
        result = self.cur.execute("SELECT * FROM employees WHERE hired = 0").fetchall()
        return result

    ################# USER SELECT FUNCTIONS#########################################
    #SELECT ALL UNREGISTERED USERS
    def select_all_unregistered_users(self):
        self.cur = self.con.self.cursor()
        result = self.cur.execute("SELECT * FROM users WHERE registered = 0").fetchall()
        return result

    def select_all_registered_users(self):
        self.cur = self.con.self.cursor()
        result = self.cur.execute("SELECT * FROM users Where registered = 1").fetchall()
        return result




        #GENERAL USER INFO
    def select_user_info(self,user_id):
        self.cur = self.con.self.cursor()
        result = self.cur.execute("SELECT * FROM users WHERE user_id = '%s'" %user_id).fetchall()
        return result

        # USERS CAN DELETE THEIR ACCOUNT IF THEY WISH TO DO SO. (MANAGERS MAY ALSO USE THIS TO REMOVE USER FROM WEBSITE)
    def delete_account(self,user_id):
        self.cur = self.con.self.cursor()
        self.cur.execute("DELETE FROM users WHERE user_id = '%s'" % user_id)
        self.con.commit()

        #TOP FIVE RATED FOODS OF USER
    def select_top_user_rated(self,user_id):
        self.cur = self.con.self.cursor()
        result = self.cur.execute(
            "SELECT menu_item,rating FROM ratings WHERE user_id = '%s' ORDER BY rate DESC LIMIT 5" % user_id).fetchall()
        return result

        #VISITORS TOP 5 RATED FOOD (GET THIS FROM ALL RATED FOOD)
    def select_top5_rated(self):
        self.cur = self.con.self.cursor()
        result = self.cur.execute ("SELECT menu_item, rating FROM ratings ORDER BY rate DESC LIMIT 5 ")
        return result



############### END OF USER SELECT FUNCTIONS#######################################
###################################################################################

########## MANAGEMENT FUNCTIONS ##########################

        #COMPLAINTS - Will be neccessary for managers to review
    def select_complaints(self,user_id):
        self.cur = self.con.self.cursor()
        result = self.cur.execute("SELECT complaint, date_posted FROM complaints WHERE user_id = '%s'" %user_id).fetchall()
        return result

        #COMPLIMENTS -Will be neccessary for managers to review
    def select_compliments(self,user_id):
        self.cur = self.con.self.cursor()
        result = self.cur.execute("SELECT compliment, date_posted FROM compliments WHERE user_id = '%s'" %user_id).fetchall()
        return result
        #Accept Registration
    def register(self,user_id):
        self.cur = self.con.self.cursor()
        self.cur.execute("UPDATE users SET registered=1 WHERE user_id = '%s'" %user_id)
        self.con.commit()

        #hire employee
    def hire_employee(self,emp_id):
        self.cur = self.con.self.cursor()
        self.cur.execute("UPDATE employees SET hired = 1 where emp_id ='%s'" %emp_id)
        self.con.commit()

    def add_demotions(self,emp_id):
        self.cur = self.con.self.cursor()
        self.cur.execute("UPDATE employees SET demotions = demotions + 1 WHERE emp_id = '%s'" %emp_id)
        self.con.commit()

    def decrease_demotions(self,emp_id):
        self.cur = self.con.self.cursor()
        self.cur.execute("UPDATE employees SET demotions = demotions - 1 WHERE emp_id = '%s'" %emp_id)
        self.con.commit()

    def check_demotions(self,emp_id):
        self.cur = self.con.self.cursor()
        result = self.cur.execute("SELECT demotions FROM employees WHERE emp_id = '%s'" %emp_id).fetchone()
        return result

    def fire_employee(self,emp_id):
        self.cur = self.con.self.cursor()
        self.cur.execute("UPDATE employees SET hired = 0 where emp_id = '%s'" %emp_id)
        self.con.commit()

        #Promoting employee increases their salary by 5 dollars.
    def check_compliments(self,emp_id):
        self.cur = self.con.self.cursor()
        result = self.cur.execute("SELECT count(*) FROM compliments WHERE emp_id = '%s'" %emp_id).fetchall()
        return result

    def promote_employee(self,emp_id):
        self.cur = self.con.self.cursor()
        self.cur.execute("UPDATE employees SET salary = salary + 5 where emp_id = '%s'" %emp_id)
        self.con.commit()

        #demoting employee
    def check_complaints(self,emp_id):
        self.cur = self.con.self.cursor()
        result = self.cur.execute("SELECT count(*) FROM complaints WHERE emp_id '%s'" %emp_id).fetchall()
        return result

    def demote_employee(self,emp_id):
        self.cur = self.con.self.cursor()
        self.cur.execute("UPDATE employees SET salary = salary - 5 WHERE emp_id = '%s'" %emp_id)
        self.con.commit()

    def confirm_complaint(self,complaint_id):
        self.cur = self.con.self.cursor()
        self.cur.execute("UPDATE complaints SET approval = 1 where complaint_id = '%s'" %complaint_id)
        self.con.commit()

    def confirm_compliment(self,compliment_id):
        self.cur = self.con.self.cursor()
        self.cur.execute("UPDATE compliment SET approval = 1 where complaint_id = '%s'" % compliment_id)
        self.con.commit()


#update warnings in users table. Do this by counting the number of true boolean values a user has in the warnings column
# of delivery info table.
    def update_warnings(self,user_id):
        self.cur = self.con.self.cursor()
        self.cur.execute("UPDATE users set warnings = (SELECT count(cust_warning) FROM deliveryinfo where user_id = '%s')"
                    %user_id)
        self.con.commit()


    def update_delivery_stat(self,order_id):
        self.cur = self.con.self.cursor()
        self.cur.execute("UPDATE deliveryinfo set status = 1 where order_id = '%s'" %order_id)
        self.con.commit()


#TESTING SOME INSERT FUNCTIONS
#insert_restaurant("1","Los Quatro Amigos", "160 self.convent Ave","3123456543", "11365")
#inserting to restaurant works
###############################
fname = "Lenny"
lname = "Gonzalez"
address = "160 self.convent Ave"
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
#insert_employees("C0003","Lenny","Gonzalez","160 self.convent Ave","1234567899","Harlem","123456789","01-01-2017",)
#inserting to employees works, just need to figure out auto emp_id creation. or have a counter in views.py and self.concatonate the first letter with counter. e.g C + counter, counter = 1
#db.insert_users(user_id,fname,lname,"poop","e.simkhayev@gmail.com",address,city,postal,phone,birthday,salary)
