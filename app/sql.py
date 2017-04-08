import sqlite3

with sqlite3.connect("losquatroamigos.db") as connection:
    c = connection.cursor()

    ##TABLES##

    #restaurant##
    c.execute('DROP TABLE if EXISTS restaurant')
    c.excute("""CREATE TABLE restaurant (
    res_id char(1) not null,
    name varchar(20) not null,
    address varchar(40) not null,
    phone char(10) not null,
    postal char(5) not null,
    PRIMARY KEY (res_id)
    )""")

    #employees##
    c.execute('DROP TABLE if EXISTS employees')
    c.execute("""""")

