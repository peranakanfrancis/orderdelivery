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
        # only let the user login if the manager has confirmed his registration
        if int(db.is_registered(user_id)[0]) == 1:
            session["user"] = user_id
            session["logged_in"] = True
            session["role"] = "user"
            return view_user_page()
        # user is not registered
        else:
            flash("A manager must register you first!")
            return showLogIn()

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

# For relogging in
@app.route('/relogin')
def relogin():
    if session["role"] == "user":
        return view_user_page()
    if session["role"] == "manager":
        return view_management_page()
    if session["role"] == "chef":
        return view_chef_page()
    if session["role"] == "deliverer":
        return view_delivery_page()


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
    flash("You Successfully Logged Out.")
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

    # contents of delivery info.
    delivery_info = db.select_incomplete_delivery_info()
    all_compl_delivery = db.select_completed_delivery_info()
    user_info = db.select_all_registered_users()


    return render_template("loginDELIVERY.html", all_delivery=delivery_info, all_users=user_info, all_compl_delivery=all_compl_delivery)

# For the Deliverer to Complete Delivery
@app.route('/fulfill/<order_num>')
def fulfill(order_num):
    db = db_connect()
    db.update_delivery_status(order_num)
    db.update_delivery_emp_id(session.get('user'), order_num)
    flash("**Order Fulfilled & Moved to Completed Orders**")
    return view_delivery_page()

# For the Deliverer to Issue a Warning
@app.route('/issue_warning/<order_num>')
def issue_warning(order_num):
    db = db_connect()
    db.add_cust_warning(order_num)
    flash("**Warning Issued**", 'error')
    return view_delivery_page()

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

    db.insert_menu(chef_id, menu_id, item_name,item_price,"")

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

    # Checks if the address is valid for geopy
    try:
        db_connect.eval_geo_coords(_address,_city,_postal)
    except: # Note This Captures All Exceptiosn
        flash("Make Sure Your Address is Correct", "error")
        return showSignUp()


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


###### DISPLAY COMPLIMENT/COMPLAINT FORM ##############

@app.route('/show_complaint_form/')
def show_complaint_form():
    db = db_connect()
    hired_employees = db.select_all_hired_employees()
    return render_template("/complaints.html", employees=hired_employees)

@app.route('/submit_complaint', methods=["GET",'POST'])
def submit_complaint():
    db = db_connect()

    employee = request.form.get("employee")
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
    db = db_connect()
    print(session.get("user"))
    return render_template("compliments.html", employees=db.select_all_hired_employees())


@app.route('/submit_compliment', methods=["GET",'POST'])
def submit_compliment():
    db = db_connect()
    # convert employee name to emp_id which is nec for insert function
    employee = request.form.get("employee")
    employee = employee.strip().split(" ")
    emp_fname = str(employee[0])
    emp_lname = employee[1]


    user = session.get("user")
    compliment = request.form.get("compliment")

# try:
    emp_id = db.select_employee_id_from_name(emp_fname, emp_lname)[0]
    print(type(user), type(emp_id), type(compliment))
    # db.insert_compliments(user, employee, compliment)
# except:
#     print("failed")
#     flash("Submission failed")
    return render_template("compliments.html", employees=db.select_all_hired_employees())
    # return redirect("/")


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
@required_roles('user')
def checkout(price, order_items):
    db = db_connect()

    user = session.get("user")
    is_user_VIP = db.select_user_VIP_status(user)

    cart = db.select_user_cart(user)
    print(cart)
    items = []
    print(len(cart))
    print(len(order_items))

    for x in range(len(cart)):
        items.append((cart[x][3],cart[x][4]))


    print(is_user_VIP)

    if is_user_VIP == 1:
        price = float(price) * .9

    items = str(items)
    try:
        db.insert_orders(user,items,price)
        db.update_user_order_count(user)
        db.update_user_cash_spent(user, price)
        db.empty_cart(user)

        order_count = db.select_user_order_count(user)
        cash_spent_so_far = db.select_user_cash_spent(user)

        #VIP check: if this last checkout allowed customer to become VIP
        if int(order_count[0]) >= 50 or float(cash_spent_so_far[0]) >= 500:
            db.set_user_VIP_status(user)

    except:
        flash("You need to login to do that")
        return showLogIn()

    db.insert_orders(user,items,price)
    db.empty_cart(session.get("user"))

    #print(len(db.select_orders()))

    # insert item into the deliveryinfo DB
    db.insert_deliveryinfo(len(db.select_orders()), 'None', session.get("user"), status="0", cust_warning="0")


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
    db.increment_compliment_count()
    # if a customer is customer is VIP, their compliments count twice as much
    is_user_VIP = db.select_user_VIP_status(session.get("user"))
    if is_user_VIP:
        pass
    #IDK what this is for. -Eddy
    # we need to check if the employee has 3 or more compliments. so we
    # use select_compliment to find out who the compliment is referring to
    print(db.select_compliment(compliment_id))
    employee = db.select_compliment(compliment_id).empl_id
    if db.check_compliments(employee) >= 3:
        db.promote_employee(employee)
        db.delete_complaint(employee)

    return view_management_page()



# Handles Any Page That Doesn't Exist
@app.errorhandler(404)
def PageNotFound(error):
    return render_template('errors/404.html'), 404


