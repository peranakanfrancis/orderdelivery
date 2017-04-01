/* General restaurant information, we might need to reference the address for deliveries*/
drop table if exists restaurant;
CREATE TABLE restaurant (
    res_id char(1) not null,
    name varchar(20) not null,
    address varchar(40) not null,
    phone char(10) not null,
    postal char(5) not null
    );
/*Employee information. Type of employee will be first char of emp_id
C: Chef
D: Delivery Person
M: Manager
*/
DROP TABLE if EXISTS employees;
CREATE TABLE employees (
    emp_id CHAR(5) not null,
    emp_fname varchar(20) not null,
    emp_lname varchar(20) not null,
    address varchar(40) not null,
    phone char(10) not null,
    city varchar(20) not null,
    ssn varchar(9) null,
    birthdate DATE not null,
    date_hired DATE not null,
    salary decimal(3,2) not null
    );

/*General User information. I think the same concept of emp_id applies here too.
First letter of user_id will distinguish user status.
V: VIP User
R: Registered User*/
DROP TABLE if EXISTS users;
CREATE TABLE users (
    user_id char(9) not null,
    user_fname varchar(20) not null,
    user_lname varchar(40) not null,
    address varchar(40) not null,
    city varchar(20) not null,
    postal char(5) not null,
    phone char(10) not null,
    memb_since DATE not null
    acc_funds decimal(7,2) not null,
    );

/*ratings of food by user will be stored here. We can count top rated food from here*/
DROP TABLE if EXISTS ratings;
CREATE TABLE foodRating (
    user_id char(9) not null,
    menu_id char(5) not null,
    rating char(1) null
    );

/*User complaints towards employees. We can count the number of complaints linked
to emp_id then make our calculations*/
DROP TABLE if EXISTS complaints;
CREATE TABLE complaints (
    user_id char(9) not null,
    emp_id char(5) not null,
    complaint text null
    );

/*User compliments. Same gist as complaints*/
DROP TABLE if EXISTS compliments;
CREATE TABLE compliments (
    user_id char(9) not null,
    emp_id char(5) not null,
    compliment text null
    );

/*Orders will have an order_id and a user_id linked to it. The name of the item ordered,
along with rating, and chef who made it*/
DROP TABLE if EXISTS orders;
CREATE TABLE orders (
    order_id int not null AUTO_INCREMENT,
    user_id char(9) not null,
    chef_id int NOT NULL,
    menu_id char(5) not null,
    menuItem varchar(20) not null,
    price decimal(5,2) not null,
    rating char(1) null,
    PRIMARY KEY (order_id)
    );

/*Chefs will have ratings stored here. e.g Take the average of all food ratings and that is the
chefs rating*/
DROP TABLE if EXISTS chefs;
CREATE TABLE chefs (
    chef_id int NOT NULL,
    emp_id char(5) NOT NULL,
    chef_rating char(1) null
    );

/*delivery information*/
DROP TABLE if EXISTS deliveryinfo;
CREATE TABLE deliveryperson (
    emp_id char(5) not null,
    user_id char(9) not null,
    user_name varchar(20) not null,
    address varchar(40) not null,
    city varchar(20) not null,
    postal char(5) not null
    cust_warning text null,

)

/*Menu items will be created here. All items will be linked to chef_id and will include
name of food item, menu which it belongs to, price, and rating.*/
DROP TABLE if EXISTS menu;
CREATE TABLE menus (
    chef_id char(5) not null,
    menu_id char(5) not null,
    item_name varchar(50) not null,
    price decimal(5,2) not null
    rating varchar(1) null
    );

