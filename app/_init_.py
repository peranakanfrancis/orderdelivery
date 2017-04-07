"""
============================
This is the main home page
============================
"""

# Third Party Imports
from flask import Flask
from flask import render_template  # for html
from flask import request  # for reading posted values

# Create Instance of Class
app = Flask(__name__)

app.config["DATABASE"] = 'losquatroamigos.db'
app.config['DEBUG'] = True


# Run HomePage
@app.route('/')
def index():
    return render_template('index.html')

# Run MenuPage
@app.route('/menu')
def showMenu():
    return render_template('Menu.html')

# Run SignUpPage
@app.route('/showSignUp')
def showRegister():
    return render_template('signup.html')

# Run Register
@app.route('/signUp')
def register():

    #read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    #validate the received values
   # if _name and _email and _password




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
