import sqlite3
from datetime import datetime, date

with sqlite3.connect("losquatroamigos.db") as connection:
    c = connection.cursor()

    ##TABLES##

    #restaurant##
    c.execute('DROP TABLE if EXISTS restaurant')
    c.execute("""CREATE TABLE restaurant (
    res_id nchar(1) not null,
    name varchar(20) not null,
    address varchar(40) not null,
    city varchar(20) not null,
    state nchar(2) not null,
    postal nchar(5) not null,
    phone nchar(10) not null,
    PRIMARY KEY (res_id)
    )""")

    #employees##
    c.execute('DROP TABLE if EXISTS employees')
    c.execute("""CREATE TABLE employees (
    emp_id VARCHAR(5) not null,
    password varchar(20) not null,
    emp_fname varchar(20) not null,
    emp_lname varchar(20) not null,
    address varchar(40) not null,
    city varchar(20) not null,
    state nchar(2) not null,
    postal char(5) not null,
    apt varchar(5),
    phone nchar(10) not null,
    ssn varchar(9),
    birthdate DATE not null,
    salary decimal(5,2) not null,
    date_hired [timestamp] timestamp,
    hired nchar(1) not null,
    demotions int,
    compliments int,
    complaints int,
    PRIMARY KEY (emp_id)
    )""")

    #users##
    c.execute('DROP TABLE if EXISTS users')
    c.execute("""CREATE TABLE users (
    user_id VARCHAR(9) not null,
    f_name varchar(20) not null,
    l_name varchar(40) not null,
    password VARCHAR(20) NOT NULL,
    address varchar(40) not null,
    city varchar(20) not null,
    state nchar(2) not null,
    postal nchar(5) not null,
    apt varchar(5),
    longitude decimal(9,6),
    latitude decimal (9,6),
    phone nchar(10) not null,
    memb_since DATE not null,
    acc_funds decimal(7,2) not null,
    registered nchar(1) not null,
    warnings int,
    PRIMARY KEY (user_id)
    )""")

    #ratings##
    c.execute('DROP TABLE if EXISTS foodrating')
    c.execute("""CREATE TABLE foodrating (
    user_id VARCHAR(9) not null,
    menu_id VARCHAR(5) not null,
    menu_item varchar(50) not null,
    rating nchar(1),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    )""")

    #complaints##
    c.execute('DROP TABLE if EXISTS complaints')
    c.execute("""CREATE TABLE complaints (
    complaint_id INTEGER PRIMARY KEY,
    user_id VARCHAR(9) not null,
    emp_id VARCHAR(5) not null,
    complaint text,
    approval nchar(1),
    date_posted [timestamp] timestamp,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
    )""")

    #compliments##
    c.execute('DROP TABLE if EXISTS compliments')
    c.execute("""CREATE TABLE compliments (
    compliment_id INTEGER PRIMARY KEY,
    user_id VARCHAR(9) NOT NULL,
    emp_id VARCHAR(5) NOT NULL,
    date_posted [timestamp] timestamp,
    compliment text,
    approval boolean,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
    )""")

    #orders##
    c.execute('DROP TABLE if EXISTS orders')
    c.execute("""CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id VARCHAR(9) not null,
    chef_id VARCHAR(5) NOT NULL,
    menu_id VARCHAR(5) not null,
    menu_Item varchar(20) not null,
    price decimal(5,2) not null,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (chef_id) REFERENCES chefs(chef_id)
    )""")

    #figuring out how autoincrement works.
    c.execute('INSERT INTO orders VALUES(NULL,"U0001","C0001","M0001","STEAK", "10.00")')
    #select_top5_ratings("U0001")


    ##chefs##chef rating will be average of all menu item ratings.
    c.execute('DROP TABLE if EXISTS chefs')
    c.execute("""CREATE TABLE chefs (
    chef_id VARCHAR(5) NOT NULL,
    emp_id VARCHAR(5) NOT NULL,
    menu_name varchar(20) NOT NULL,
    chef_rating nchar(1),
    PRIMARY KEY (chef_id),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
    )""")

    ##delivery information##
    c.execute('DROP TABLE if EXISTS deliveryinfo')
    c.execute("""CREATE TABLE deliveryinfo (
    order_id INT PRIMARY KEY,
    emp_id VARCHAR(5) not null,
    user_id VARCHAR(9) not null,
    status ncahr(1) not null,
    cust_warning boolean,
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    )""")

    ##menu/menu items##
    c.execute('DROP TABLE if EXISTS menus')
    c.execute("""CREATE TABLE menus (
    chef_id VARCHAR(5) not null,
    menu_id VARCHAR(5) not null,
    item_name text not null,
    price decimal(5,2) not null,
    rating varchar(1),
    FOREIGN KEY (chef_id) REFERENCES chefs(chef_id)
    )""")

    ##sample data!##
    #RESTAURANT##
    c.execute('INSERT INTO restaurant VALUES("1","Los Quatro Amigos","160 Convent Ave","New York","NY","10031","2126507000")')

    ##END OF RESTAURANT DATA###

    ##EMPLOYEES##
    ##CHEFS##
        #CHEF JUAN#
    c.execute('INSERT INTO employees VALUES ("C1","pizza","Juan","Gonzalez","160 Convent Ave",'
              '"New York","NY", "10031","4L","2126507000","123456789","1985-05-21","25.50","2017-01-01", 1,0,0,0)')
    c.execute('INSERT INTO chefs VALUES ("1","C1","Juan\'s Mole","")')

        #CHEF MIGGY#
    c.execute('INSERT INTO employees VALUES ("C2","pizza","Miguel","Dominguez","160 Convent Ave",'
              '"New York", "NY", "10031", "5L","2126507000","123456789","1979-02-02","25.50","2017-01-01", 1,0,0,0)')
    c.execute('INSERT INTO chefs VALUES("2","C2","Miggy\'s Seafood","")')

        #Chef Monica#
    c.execute('INSERT INTO employees VALUES ("C3","pizza","Monica","Gonzalez","160 Convent Ave",'
              '"New York","NY", "10031","6L","2126507000","123456789","1991-08-21","25.50","2017-01-01", 1,0,0,0)')
    c.execute('INSERT INTO chefs VALUES ("3","C3","Monica\'s Sweets","")')

        #Chef Rosita#
    c.execute('INSERT INTO employees VALUES ("C4","pizza","Rosita","Rodriguez","160 Convent Ave",'
              '"New York","NY", "10031","2L","2126507000","123456789","1980-05-21","25.50","2017-01-01", 1,0,0,0)')
    c.execute('INSERT INTO chefs VALUES ("4","C4","Rosita\'s Gill Grill","") ')

    ##Delivery Personnel##

        #Delivery Boy Dave
    c.execute('INSERT INTO employees VALUES ("D1","pizza","David","Jones","160 Convent Ave",'
              '"New York","NY", "10031","4A","2126507000","123456789","1994-08-21","10.50","2017-01-01", 1,0,0,0)')

        #Delivery Boy Max
    c.execute('INSERT INTO employees VALUES ("D2","pizza","Max","Young","160 Convent Ave",'
              '"New York","NY", "10031","2P","2126507000","123456789","1990-09-11","10.50","2017-01-01", 1,0,0,0)')

    ##END OF DELIVERY PERSONNEL DATA##

    ##Managers##
        #Manager Emily#
    c.execute('INSERT INTO employees VALUES ("M1","pizza","Emily","Dickerson","160 Convent Ave",'
              '"New York","NY", "10031","4B","2126507000","123456789","1985-01-21","27.50","2017-01-01", 0,0,0,0)')

        #Manager Jeff#
    c.execute('INSERT INTO employees VALUES ("M2","pizza","Jeff","Edwards","160 Convent Ave",'
              '"New York","NY", "10031","1C","2126507000","123456789","1994-08-21","10.50","2017-01-01", 0,0,0,0)')

    ###### END OF MANAGER DATA##

    ### END OF EMPLOYEES DATA##

    #MENUS/MENU ITEMS

        #CHEF MIGUEL#
    #insert_menu(chef_id, menu_id, item_name, price, rating)
    c.execute('INSERT INTO menus VALUES '
              '("C2","1","Taco","6.00","3"),'
              '("C2","2","Bistec (Steak)","14.00","2"),'
              '("C2","3","Pollo (Chicken)","11.00","4"),'
              '("C2","4","Chorizo (Sausage)","9.00","5"),'
              '("C2","5","Cecina (Jerky Style Beef)","13.00","5"),'
              '("C2","6","Carnita (Deep Fried Pork)","9.00","3"),'
              '("C2","7","Lenuga (Beef Tounge)","12.00","4"),'
              '("C2","8","Tortas (Sandwich)","9.00","1"),'
              '("C2","9","Queso Blanco (Fresh White Cheese)","5.00","3"),'
              '("C2","10","Milanesa (Breaded Steak)","15.00","4"),'
              '("C2","11","Jamon (Ham)","11.00","4"),'
              '("C2","12","Carne Enchilada (Hot and Spicy Pork)","14.00","4")')

        #CHEF MONICA#
    c.execute('INSERT INTO menus VALUES '
              '("C3","1","Lobster Ceviche","24.00","2"),'
              '("C3","2","Yellowtail Sashimi with Dry Miso and Yuza Sauce","24.00","2"),'
              '("C3","3","Shiromi Usuzukari","9.00","4"),'
              '("C3","4","Bigeye Tuna Tataki with Tosazu","19.00","4"),'
              '("C3","5","sea Urchin Tempura","9.00","4"),'
              '("C3","6","Rock Shrimp Tempura with Ponzu","11.00","5"),'
              '("C3","7","Chilean Sea Bass with Black Bean Sause","24.00",""),'
              '("C3","8","Lobster with Wasabi Pepper Sause","28.00","5"),'
              '("C3","9","Kaki Age Donburi","16.00","4"),'
              '("C3","10","Tempura Donburi","14.00","4"),'
              '("C3","11","Ribeye Anticucho","21.00","3")')

        #CHEF Rosita#
    c.execute('INSERT INTO menus VALUES '
              '("C4","1","Hot Plate Combinations","19.00","3"),'
              '("C4","2","Pechuga De Pollo A La Parrilla (Grilled Chicken Cutlet)","12.00","4"),'
              '("C4","3","Milanesa De Res (Breaded Steak)","15.00","4"),'
              '("C4","4","Carne Enchilada (Hot and Spicy Pork)","14.00","4"),'
              '("C4","5","Medio Pollo Rostizado (Half Roasted Chicken)","12.00","4"),'
              '("C4","6","Pernil Horneado (Roasted Pork)","14.00","4"),'
              '("C4","7","Bistec Encebollado (Steak with Onions)","17.00","3"),'
              '("C4","8","Carne De Cecina (Jerky Beef Steak)","13.00","5"),'
              '("C4","9","Mole Poblano (Chicken with Mole)","15.00","5")')

    #USERS###
    #template:(user_id, user_fname, user_lname, password, email, address, city, state, postal, apt, phone, memb_since, acc_funds)
    # c.execute('INSERT INTO users VALUES '
    #           '("woozycake","Kristen","Sedor","a1lk3j4","frostman@att.net","580 St Nicholas Ave","New York","NY","10030","4L","2121234567","2017-01-01","50.00"),'
    #           '("waryquiche","Chance","Mee","LK0912","mbrown@icloud.com","69-92 Edgecombe Ave","New York","NY","10030","2M","2121234567","2017-01-01","50.00"),'
    #           '("poisedpolenta","Minna","Sapien","PO23ks","gemmell@att.net","1649 Amsterdam Ave","New York","NY","10031","7C","2127696649","2017-01-01","50.00"),'
    #           '("trainedsyrup","George","Loller","LOsaM3","zeller@mac.com","630 St Nicholas Ave","New York","NY","10030","2L","2122190755","2017-01-01","50.00"),'
    #           '("jazzycheese","Brendon","Pulsifer","LJk5k","dleconte@optonline.net","1508 Amsterdam Ave","New York","NY","10031","2P","2123491649","2017-01-01","50.00"),'
    #           '("highapples","Ernie","Sol","M1N3l","bigmauler@outlook.com","1518 Amsterdam Ave","New York","NY","10031","7D","2121654987","2017-01-01","50.00"),'
    #           '("cuddlyrice","Antoinette","Tropoea","mK2n3","wkrebs@icloud.com","1701 Amsterdam Ave","New York","NY","10031","3C","2126597316","2017-01-01","50.00"),'
    #           '("draftyclam","Gergory","Crane","oL245","jandrese@att.net","628-628 Riverside Dr","New York","NY","10031","4T","2124697315","2017-01-01","50.00"),'
    #           '("thesedoughnuts","Dorie","Chastain","0n9n1","raines@sbcglobal.net","601-625 W 133rd St","New York","NY","10027","3D","2127986459","2017-01-01","50.00"),'
    #           '("screechinglard","Graciela","Winfrey","en34l","kingjoshi@outlook.com","2450 Frederick Douglass Blvd","New York","NY","10027","8C","2126482379","2017-01-01","50.00"),'
    #           '("vitalchile","Lashawn","Lafleur","y1x23","fbriere@yahoo.com","501 W 133rd St","New York","NY","10027","2C","2124578126","2017-01-01","50.00"),'
    #           '("gaseoussausage","Bettina","Molter","4k2k1","eabrown@msn.com","603 W 129th St","New York","NY","10027","4D","2129878654","2017-01-01","50.00")')
