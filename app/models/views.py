from app import app
from flask import render_template,redirect, request, flash,g,session,url_for,json
from app.models.models import *



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
    user_id = request.form['username']
    password = request.form['password']

    user_check = select_user_info(user_id)
    empl_check = select_employee_info(user_id)
    #print(empl_check)
    #print(empl_check[0][0][0])


    if user_check and user_check[0][3] == password:
        session["user"] = user_id
        session["logged_in"] = True
        return render_template("loginUSER.html")

    if empl_check[0][0][0] == 'M':
        print("logged in as manager")
        #this is a manager.
        return render_template("loginUSER.html")

    if empl_check[0][0][0] == 'C':

        # this is a chef
        return render_template("/")
    if empl_check[0][0][0] == 'D':
        # this is a delivery guy
        return render_template("/")



    else:
        flash("Login Failed :(")
        return render_template("Log-In.html")

# Controlling Logging Out
@app.route('/logout/')
def logout():
    # remove the un from the session if it is there
    session.pop('user', None)
    session["logged_in"] = False
    return redirect('/')

@app.route('/show_complaint_form')
def show_complaint_form():
    return render_template("complaints.html")

@app.route('/submit_complaint', methods=["GET",'POST'])
def submit_complaint():
    chef = request.form["chef"]
    user = session['user']
    complaint = request.form["complaint"]
    try:
        insert_complaints(user,chef,complaint)
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
        insert_compliments(user,chef,compliment)
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
@app.route('/sign_up/', methods=["GET",'POST'])
def sign_up():
    #read the values from the UI
    _user_id = request.form['inputName']
    _password = request.form['inputPassword']

    try:
        insert_users(_user_id,"bob", "who", _password, "137-10 Geranium Avenue Flushing NY 11355",
                    "Flushing", "NY", "11355", "", 6469825000)
        session["user"] = _user_id
    except:
        return render_template("signup.html")

    #validate the received values
   # if _name and _email and _password
    return redirect("/")

@app.route('/loginManager')
def view_management_page():
    unregistered_users = select_all_unregistered_users()
    registered = select_all_registered_users()
    hired_employees = select_all_hired_employees()
    unhired_employees = select_all_pending_employees()

    return render_template("loginMANAGER.html", registered_users=registered, unregistered=unregistered_users, hired_employees=hired_employees, unhired_employees=unhired_employees )

# EMPLOYEE MANAGEMENT TOOLS
@app.route('/accept_user/<user>', methods=['GET'])
def accept_user(user):
    register(user)
    return view_management_page()

@app.route('/hire_chef/<chef>', methods=['GET'])
def hire_employee(empl_name):
    hire(empl_name)
    return view_management_page()

@app.route('/fire_chef/<chef>', methods=['GET'])
def fire_employee(empl_name):
    fire(empl_name)
    return view_management_page()


@app.route('/promote_chef/<chef>', methods=['GET'])
def promote_employee(empl_name):
    promote(empl_name)
    return view_management_page()

@app.route('/demote_chef/<chef>', methods=['GET'])
def demote_employee(empl_name):
    demote(empl_name)
    if select_demote_count(empl_name) > 1:
        fire(empl_name)
    return view_management_page()

@app.route('/add_warning/<user>', methods=['GET'])
def add_warning(user_id):
    add_warning_to(user_id)
    return view_management_page()

@app.route('/add_complaint/<user>', methods=['GET'])
def accept_complaint(complaint_id):
    confirm_complaint(complaint_id)
    employee = select_complaint(complaint_id).empl_id
    if check_complaints(employee) >= 3:
        demote_employee(employee)

        if count_demotions(employee) >= 2:
            fire_employee(employee)

    return view_management_page()

@app.route('/add_compliment/<user>', methods=['GET'])
def accept_compliment(compliment_id):
    confirm_compliment(compliment_id)
    employee = select_compliment(compliment_id).empl_id
    if check_compliments(employee) >= 3:
        promote_employee(employee)
    delete_complaint(employee)

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
