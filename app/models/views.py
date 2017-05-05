from app import app
from flask import render_template,redirect, request, flash,g,session,url_for,json
from app.models.models import db_connect

###db_connect contains all query methods##
db = db_connect()
#########################################3

# Run HomePage
@app.route('/')
def index():
    print(session.get("user"))
    return render_template('index.html')


# Run LogInPage
@app.route('/showLogIn/')
def showLogIn():
    if not session.get('logged_in'):
        return render_template('Log-In.html')
    else:
        return render_template("loginUSER.html")
    #replace this with the designated customer/chef/ manager


@app.route('/login', methods=["GET",'POST'])
def login():
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
        return render_template("loginUSER.html")

    if empl_check[0][0] == 'M' and empl_check[1] == password:
        session["logged_in"] = True
        return render_template("loginMANAGER.html")

    if empl_check[0][0] == 'C' and empl_check[1] == password:
        session["logged_in"] = True
        return render_template("loginCHEF.html")

    if empl_check[0][1] == 'D' and empl_check[1] == password:
        session["logged_in"] = True
        return render_template("loginDELIVERY.html")

    else:
        flash("Login Failed :(")
        return render_template("Log-In.html")

# Controlling Logging Out
@app.route('/logout/')
def logout():
    # remove the un from the session if it is there
    session.pop('user', None)
    session["logged_in"] = False
    return render_template("index.html")

@app.route('/show_complaint_form')
def show_complaint_form():
    return render_template("complaints.html")

@app.route('/submit_complaint', methods=["GET",'POST'])
def submit_complaint():
    chef = request.form["chef"]
    user = session['user']
    complaint = request.form["complaint"]
    try:
        db.insert_complaints(user,chef,complaint)
    except:
        flash("Submittion failed")
        return render_template("complaints.html")
    return redirect("/")

@app.route('/show_compliment_form')
def show_compliment_form():
    return render_template("compliments.html")


@app.route('/submit_compliment', methods=["GET",'POST'])
def submit_compliment():
    chef = request.form["chef"]
    user = session['user']
    compliment = request.form["compliment"]
    try:
        db.insert_compliments(user,chef,compliment)
    except:
        print("failed")
        flash("Submittion failed")
        return render_template("compliments.html")
    return redirect("/")


# Authenticate LogIn
@app.route('/manager_login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return showLogIn()



# Run MenuPage
@app.route('/menu/')
def showMenu():
    return render_template('Menu.html')

# Run SignUpPage
@app.route('/showSignUp/')
def showSignUp():
    return render_template('signup.html')

# Run Juan Menu
@app.route('/Juan_Menu/')
def Juan_Menu():
    # if session.get('logged_in'):
    #     top_menu = select_top5_rated()

    return render_template('Juan_Menu.html')


# Run miguel Menu
@app.route('/miguel_Menu/')
def miguel_Menu():
    return render_template('Menu.html')

# Run Rosita Menu
@app.route('/Rosita_Menu/')
def Rosita_Menu():
    return render_template('Rosita_Menu.html')

# Run monica Menu
@app.route('/monica_Menu/')
def monica_Menu():
    return render_template('monica_Menu.html')

# Run Register
@app.route('/signup/', methods=["GET",'POST'])
def sign_up():
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

    # If the username exists
    if user_check and user_check[0][0] == _userName:
        flash("Sorry, Username Exists", 'error')
        return render_template("signup.html")
    # If the key fields are not entered
    elif not _firstName or not _lastName or not _userName or not _password or not _address or not _city or not _state:
        flash("Please Enter All Info with Asterisks")
        return render_template("signup.html")
    # Insert User
    else:
        db.insert_users(_userName, _firstName, _lastName, _password, _address, _city, _state, _postal, _apt, _phone, acc_funds=0)
        return render_template("loginUSER.html")



@app.route('/loginManager')
def view_management_page():
    unregistered_users = db.select_all_unregistered_users()
    registered = db.select_all_registered_users()
    hired_employees = db.select_all_hired_employees()
    unhired_employees = db.select_all_pending_employees()

    return render_template("loginMANAGER.html", registered_users=registered, unregistered=unregistered_users, hired_employees=hired_employees, unhired_employees=unhired_employees )

# EMPLOYEE MANAGEMENT TOOLS
@app.route('/accept_user/<user>', methods=['GET'])
def accept_user(user):
    db.register(user)
    return view_management_page()

@app.route('/hire_employee/<empl_name>', methods=['GET'])
def hire(empl_name):
    db.hire_employee(empl_name)
    return view_management_page()

@app.route('/fire/<empl_name>', methods=['GET'])
def fire(empl_name):
    db.fire_employee(empl_name)
    return view_management_page()

@app.route('/upgrade_user/<user>', methods=['GET'])
def upgrade(empl_name):
    db.upgrade_user(empl_name)
    return view_management_page()


@app.route('/promote/<empl_name>', methods=['GET'])
def promote(empl_name):
    db.promote_employee(empl_name)
    return view_management_page()

@app.route('/demote/<empl_name>', methods=['GET'])
def demote(empl_name):
    db.add_demotions(empl_name)
    db.demote_employee(empl_name)
    print(db.check_demotions(empl_name)[0])
    if db.check_demotions(empl_name)[0] > 1:
        db.fire_employee(empl_name)
    return view_management_page()

@app.route('/add_warning/<user>', methods=['GET'])
def add_warning(user_id):
    db.update_warnings(user_id)
    return view_management_page()

@app.route('/add_complaint/<complaint_id>', methods=['GET'])
def accept_complaint(complaint_id):
    db.confirm_complaint(complaint_id)
    #I dk what this is for. -Eddy
    employee = db.select_complaint(complaint_id).empl_id
    if db.check_complaints(employee) >= 3:
        db.demote_employee(employee)

        if db.check_demotions(employee) >= 2:
            db.fire_employee(employee)

    return view_management_page()

@app.route('/decline_complaint/<complaint_id>', methods=['GET'])
def decline_complaint(complaint_id):
    db.delete_complaint(complaint_id)
    user = db.select_user_from_complaint(complaint_id)
    db.update_warnings(user)
    return view_management_page()

@app.route('/add_compliment/<user>', methods=['GET'])
def accept_compliment(compliment_id):
    db.confirm_compliment(compliment_id)
    #IDK what this is for. -Eddy
    '''
    The chef whose dishes received consistently low ratings or 3 complaints, or no order at

    all for 3 days, will be demoted (less salary), a chef demoted twice is fired. Conversely, a

    chef whose dishes received high ratings or 3 compliments, will be promoted (higher

    salary). One compliment can be used to cancel one complaint. The delivery people are

    handled the same way.
    
    '''

    #let me know if im misreading something
    employee = db.select_compliment(compliment_id).empl_id
    if db.check_compliments(employee) >= 3:
        db.promote_employee(employee)
        db.delete_complaint(employee)

    return view_management_page()



# Handles Any Page That Doesn't Exist
@app.errorhandler(404)
def PageNotFound(error):
    return render_template('errors/404.html'), 404


#Import all of our routes from routes.py
    #from routes import *;

#For Dynamic Pages Per User
    #name is generated with the dynamic argument
#@app.route('/user/<name>'):
#def user(name):
    #return '<h1>Hey, %s!</h1>' % name


#Develop Web Server
#if __name__ == "__main__":
    #app.secret_key = os.urandom(12)
 #   app.run(debug=True)
