from app import app
from flask import render_template,redirect, request, flash,g,session,url_for,json, Response
from app.models.models import db_connect
from .forms import *
from functools import wraps # for the role_required decorator
import json
###db_connect contains all query methods##
#db = db_connect()
#########################################3

###### LOGIN ########

# Run HomePage
@app.route('/')
def index():
    db = db_connect() # connect to the database
    #print(session.get("user"))
    return render_template('index.html', top_five=db.select_top5_rated())


# Run LogInPage
@app.route('/showLogIn/')
def showLogIn():
    return render_template("Log-In.html")


# Login Logic
@app.route('/login', methods=["GET",'POST'])
def login():
    db = db_connect()
    # Get details from the user
    user_id = request.form['username']
    password = request.form['password']

    # Get details from the db
    user_check = db.select_user_info(user_id)
    empl_check = db.select_employee_info(user_id)

    # Check user details against db
    if user_check and user_check[0][3] == password:
        session["user"] = user_id
        session["logged_in"] = True
        session["role"] = "user"
        return view_user_page()

    if empl_check and empl_check[0][0] == 'M' and empl_check[1] == password:
        session["user"] = user_id
        session["logged_in"] = True
        session["role"] = "manager"
        return view_management_page()

    if empl_check and empl_check[0][0] == 'C' and empl_check[1] == password:
        session["user"] = user_id
        session["logged_in"] = True
        session["role"] = "chef"
        return view_chef_page()

    if empl_check and empl_check[0][0] == 'D' and empl_check[1] == password:
        session["user"] = user_id
        session["logged_in"] = True
        session["role"] = "deliverer"
        return view_delivery_page()

    else:
        flash("Login Failed :(")
        return showLogIn()


# Role Checking Decorator to Ensure Only Eligible User Has Access
def required_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_current_user_role() not in roles:
                flash('Authentication error, please check your details and try again', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)

        return wrapped

    return wrapper

# Get User
def get_current_user_role():
    return session.get('role')

# Controlling Logging Out
@app.route('/logout/')
def logout():

    # remove the un from the session if it is there
    session.pop('user', None)
    session.pop('role', None)
    session["logged_in"] = False
    return index()


# LOGIN AS DELIVERY PERSONS
@app.route('/loginDelivery')
@required_roles('deliverer')
def view_delivery_page():
    db = db_connect()
    # change all_orders later....
    #whichever delivery person is logged in will take an order.

    delivery_person = session.get('user')
    orders = db.select_orders()

    #add over items in orders to delivery page.
    for x in range(len(orders)):
        db.insert_deliveryinfo(orders[x][0],delivery_person,orders[x][1],status="0",cust_warning="0")
        db.delete_order(orders[x][0])

    #contents of delivery info.
    delivery_info = db.select_delivery_info()

    #useful model functions:
    #delete_order(order_id) - deletes order based off order #
    #update_delivery_status(order_id) -changes delivery status to 1 (delivered)
    #add_cust_warning(order_id) - changes cust_warning to 1
    #delete_delivery_items() - deletes all items where status is 1.

    return render_template("loginDELIVERY.html", all_orders=db.select_user_info('test'))


# LOGIN AS USER
@app.route('/loginUser/')
@required_roles('user')
def view_user_page():
    db = db_connect()
    # user_top_five = db.select_top5_rated() -- wait to orders is done
    return render_template("loginUSER.html", top_five=db.select_top5_rated(), orders=db.select_user_orders(session.get("user")))

# LOGIN AS CHEF -- make SURE TO INCLUDE SOME SECURITY
@app.route('/loginChef')
@required_roles('chef')
def view_chef_page():
    db = db_connect()
    print(session.get('user'))
    chef_name = db.select_chef_session(session.get('user'))
    print(chef_name)
    menu = db.select_chef_menu()

    return render_template("loginCHEF.html", menu_info = menu, chef = chef_name)

#@app.route('/saveMenuChanges/<updatedmenu>')
#def SaveMenuChanges(updatedmenu):
#    db = db_connect()
#    menu = request.form["menu"]
#    return view_chef_page()

@app.route('/editMenu/<curr_item>/<curr_price>', methods=['POST'])
def editMenu(curr_item,curr_price):

    db = db_connect()

    new_item = request.form['_menu']
    new_price = request.form['price']
    print(new_item)
    print(curr_item)
    print(curr_price)

    db.update_menu_item(new_item,curr_item)
    db.update_menu_price(new_price,curr_item)

    return view_chef_page()

@app.route('/delete_menu_item/<item_name>')
def delete_menu_item(item_name):
    db = db_connect()
    print(item_name)
    db.delete_menu_item(item_name)
    return view_chef_page()

@app.route('/add_menu_item/<chef>', methods=['POST'])
def add_menu_item(chef):
    db = db_connect()

    item_name = request.form['new_item']
    item_price = request.form['new_price']

    chef_id = session.get('user')

    menu_id = db.select_menu_id(chef_id)
    print(chef_id)
    print(menu_id)
    #menu_id = (menu_id)
    print(item_price)
    print(item_name)

    if menu_id[0] ==None:
        menu_id = str(0)
    else:
        menu_id = str(int(menu_id[0]) + 1)

    db.insert_menu(chef_id,menu_id,item_name,item_price,"")

    return view_chef_page()

# LOGIN AS MANAGER
@app.route('/loginManager')
@required_roles('manager')
def view_management_page():
    db = db_connect()

    unregistered_users = db.select_all_unregistered_users()
    registered = db.select_all_registered_users()
    hired_employees = db.select_all_hired_employees()
    unhired_employees = db.select_all_pending_employees()
    list_of_complaints = db.select_all_pending_complaints()

    return render_template("loginMANAGER.html", registered_users=registered, unregistered=unregistered_users,
                           hired_employees=hired_employees, unhired_employees=unhired_employees, complaints=list_of_complaints )

# Run SignUpPage
@app.route('/showSignUp/')
def showSignUp():
    db = db_connect()

    return render_template('signup.html')


# Run Register
@app.route('/signup/', methods=["GET",'POST'])
def sign_up():
    db = db_connect()
    # read the values from the UI
    _firstName = request.form['first_name']
    _lastName = request.form['last_name']
    _userName = request.form['user_name']
    _password = request.form['password']
    _address = request.form['address']
    _city = request.form['city']
    _state = request.form['state']
    _postal = request.form['postal']
    _apt = request.form['apt']
    _phone = request.form['phone']

    # Check if username exists
    user_check = db.select_user_info(_userName)

    try:
        # If the username exists
        if user_check and user_check[0][0] == _userName:
            flash("Sorry, Username Exists", 'error')
            return showSignUp()
        # If the key fields are not entered
        elif not _firstName or not _lastName or not _userName or not _password or not _address or not _city or not _state:
            flash("Please Enter All Info with Asterisks")
            return showSignUp()
        # Insert User
        else:
            db.insert_users(_userName, _firstName, _lastName, _password, _address, _city, _state, _postal, _apt, _phone, acc_funds=0)
            session["user"] = _userName
            session["logged_in"] = True
            session["role"] = "user"
            return view_user_page()
    except: # NOTE THIS CAPTURES ALL EXCEPTIONS
        flash("Make Sure Your Address is Correct", "error")
        return showSignUp()

###### DISPLAY COMPLIMENT/COMPLAINT FORM ##############

@app.route('/show_complaint_form/')
def show_complaint_form():
    db = db_connect()
    hired_employees = db.select_all_hired_employees()
    return render_template("/complaints.html", employees=hired_employees)

@app.route('/submit_complaint', methods=["GET",'POST'])
def submit_complaint():
    db = db_connect()

    employee = request.form["employee"]
    employee = employee.strip().split(" ")
    emp_fname = str(employee[0])
    emp_lname = employee[1]
    emp_id = db.select_employee_id_from_name(emp_fname, emp_lname)[0]

    user = "Lenny"
    complaint = request.form["complaint"]
    try:
        db.insert_complaints(user,emp_id,complaint)
    except:
        flash("Submittion failed")
        return render_template("complaints.html")
    return redirect("/")

@app.route('/show_compliment_form')
def show_compliment_form():
    return render_template("compliments.html")


@app.route('/submit_compliment', methods=["GET",'POST'])
def submit_compliment():
    db = db_connect()
    chef = request.form["chef"]
    user = session['user']
    compliment = request.form["compliment"]
    try:
        db.insert_compliments(user, chef, compliment)
    except:
        print("failed")
        flash("Submittion failed")
        return render_template("compliments.html")
    return redirect("/")


######### MENU SECTION ###########

# Run MenuPage
@app.route('/menu', methods=["GET",'POST'])
def showMenu():
    db = db_connect()

    try:
        items_in_cart = db.select_user_cart(session.get("user"))
    except:
        items_in_cart = []
    total_price = 0
    for item in items_in_cart:
        item_price = db.select_menu_price(item[1],item[2])
        # total price so far = price * quantity
        total_price += item_price[0] * item[4]
    return render_template('Menu.html',databaseitems = db.select_menu_items(),numbers=db.select_menu_rating_numbers(),
                           menu_items=db.select_menu(), cart=items_in_cart, sum_of_items=total_price, user_id=session.get("user"))

@app.route('/add_to_cart', methods=["GET",'POST'])
def add_to_cart():
    db = db_connect()
    # taken from menu form
    list_of_quantities = request.form.getlist("quantity")

    menu_items = db.select_menu()
    # loop through quantity list and list of menu items simultaneously
    # the index value value should match up, so the first quantity should be referring to
    # the first quantity in list of menu

    for count,menu_item in zip(list_of_quantities,menu_items):
        # if the quantity from the menu form is not empty we convert it to an integer and
        # insert it into the cart
        if count != '':

            quantity = int(count)
            try:

                db.insert_cart_items(session.get("user"), menu_item[0], menu_item[2], menu_item[3], quantity)
            except:
                flash("You need to login to do that")
                return showLogIn()

    return showMenu()

@app.route('/checkout/<price>/<order_items>', methods=["GET",'POST'])
def checkout(price, order_items):
    db = db_connect()
    try:
        db.insert_orders(session.get("user"),order_items,price)
        db.empty_cart(session.get("user"))
    except:
        flash("You need to login to do that")
        return showLogIn()

    return render_template("Order Confirmation.html", order=order_items, total_price=price)

@app.route('/show_ratings', methods=["GET",'POST'])
def show_ratings():
    db = db_connect()

    return render_template("ratings.html", databaseitems = db.select_menu_items(),numbers=db.select_menu_rating_numbers(),
                           menu_items=db.select_menu())

@app.route('/submit_rating', methods=["GET",'POST'])
def submit_rating():
    db = db_connect()
    rating = request.form["rating"]

    chef_id = request.values["chef_id"]
    menu_id = request.values["menu_id"]

    if rating != '':
        db.insert_ratings(chef_id,menu_id,rating)
    else:
        flash("enter a number")

    return show_ratings()

# EMPLOYEE MANAGEMENT TOOLS
@app.route('/accept_user/<user>', methods=['GET'])
def accept_user(user):
    db = db_connect()
    db.register(user)
    return view_management_page()


@app.route('/hire_employee/<empl_name>', methods=['GET'])
def hire(empl_name):
    db = db_connect()
    db.hire_employee(empl_name)
    return view_management_page()

@app.route('/fire/<empl_name>', methods=['GET'])
def fire(empl_name):
    db = db_connect()
    db.fire_employee(empl_name)
    return view_management_page()

@app.route('/upgrade_user/<user>', methods=['GET'])
def upgrade(empl_name):
    db = db_connect()
    db.upgrade_user(empl_name)
    return view_management_page()


@app.route('/promote/<empl_name>', methods=['GET'])
def promote(empl_name):
    db = db_connect()
    db.promote_employee(empl_name)
    return view_management_page()

@app.route('/demote/<empl_name>', methods=['GET'])
def demote(empl_name):
    db = db_connect()
    db.add_demotions(empl_name)
    db.demote_employee(empl_name)
    print(db.check_demotions(empl_name)[0])
    try:
        if db.check_demotions(empl_name)[0] > 1:
            db.fire_employee(empl_name)
    except:
        return view_management_page()
    return view_management_page()

@app.route('/add_warning/<user>', methods=['GET'])
def add_warning(user_id):
    db = db_connect()
    db.update_warnings(user_id)
    return view_management_page()

@app.route('/accept_complaint/<complaint_id>/<emp_id>', methods=['GET'])
def accept_complaint(complaint_id, emp_id):
    db = db_connect()
    db.confirm_complaint(complaint_id)
    #I dk what this is for. -Eddy
    employee = emp_id
    if db.check_complaints(employee)[0][0] >= 3:
        db.demote_employee(employee)

        if db.check_demotions(employee)[0] >= 2:
            db.fire_employee(employee)

    return view_management_page()

@app.route('/decline_complaint/<complaint_id>/<user_id>', methods=['GET'])
def decline_complaint(complaint_id,user_id):
    db = db_connect()
    db.delete_complaint(complaint_id)

    db.update_warnings(user_id)
    return view_management_page()

@app.route('/add_compliment/<user>', methods=['GET'])
def accept_compliment(compliment_id):
    db = db_connect()
    db.confirm_compliment(compliment_id)
    #IDK what this is for. -Eddy
    # we need to check if the employee has 3 or more compliments. so we
    # use select_compliment to find out who the compliment is referring to
    employee = db.select_compliment(compliment_id).empl_id
    if db.check_compliments(employee) >= 3:
        db.promote_employee(employee)
        db.delete_complaint(employee)

    return view_management_page()



# Handles Any Page That Doesn't Exist
@app.errorhandler(404)
def PageNotFound(error):
    return render_template('errors/404.html'), 404


