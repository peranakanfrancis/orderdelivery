'''
============================
This is the main home page
============================
'''

from flask import Flask, render_template, request
app = Flask(__name__)  # create instance of class

app.config["DATABASE"] = 'losquatroamigos.db'
app.config['DEBUG'] = True

# don't know what this stuff is for.
# app.config["SECRET_KEY"] = "like I'd tell you"
# app.config["USERNAME"] = "Eric"
# app.config["PASSWORD"] = "Schles"

# Chin - commented out the bottom
# from app import views, models

#Run HomePage
@app.route('/')
def index():
    return render_template('signup.html')



#For Dynamic Pages Per User
    #name is generated with the dynamic argument
#@app.route('/user/<name>'):
#def user(name):
    #return '<h1>Hey, %s!</h1>' % name


#Develop Web Server
if __name__ == "__main__":
    app.run(debug=True)