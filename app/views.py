from app import app
from flask import render_template,redirect, request, flash,g,session,url_for,json
from .models.models import *



# Run HomePage
@app.route('/')
def index():
    print(session.get("user"))
    return render_template('index.html')


# Run LogInPage replace all log-in with create-account
@app.route('/showLogIn/')
def showLogIn():
    if not session.get('logged_in'):
        return render_template('Log-In.html')
    else:
        return render_template("managerLogIn.html")

@app.route('/login', methods=["GET",'POST'])
def login():
    user_id = request.form['username']
    password = request.form['password']

    user_check= select_user_info(user_id)

    if user_check and user_check[0][3] == password:
        session["user"] = user_id
        session["logged_in"] = True
        return redirect("/")
    else:
        flash("Login Failed :(")
        return render_template("Log-In.html")

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
