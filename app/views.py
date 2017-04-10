from app import app
from flask import render_template,redirect, request, flash,g,session,url_for
from models import *


# Run HomePage
@app.route('/')
def index():
    return render_template('index.html')

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
    return render_template('Juan_Menu.html')

# Run Register
@app.route('/signUp/')
def signUp():

    #read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    #validate the received values
   # if _name and _email and _password

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
if __name__ == "__main__":
    app.run(debug=True)
