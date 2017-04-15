from app import app
from flask import render_template,redirect, request, flash,g,session,url_for,json
from models.models import *
# import models as dbHandler


# Run HomePage
@app.route('/')
def index():
    return render_template('index.html')

# Run LogInPage
@app.route('/showLogIn/')
def showLogIn():
    if not session.get('logged_in'):
        return render_template('Log-In.html')
    else:
        return render_template("managerLogIn.html")




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
    print(session.get('session_id'))
    return render_template('Juan_Menu.html')

# Run miguel Menu
@app.route('/miguel_Menu/')
def miguel_Menu():
    return render_template('miguel_Menu.html')

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
    print("here")
    #read the values from the UI
    _user_id = request.form['inputName']
    _password = request.form['inputPassword']

    insert_users(_user_id,"bob", "who", _password, "137-10 Geranium Avenue Flushing NY 11355",
                "Flushing", "NY", "11355", "", 6469825000)


    #validate the received values
   # if _name and _email and _password
    return render_template("index.html", username=_user_id)

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
