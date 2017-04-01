from flask import Flask

app = Flask(__name__)

app.config["DATABASE"] = 'losquatroamigos.db'
app.config['DEBUG'] = True

#don't know what this stuff is for.
#app.config["SECRET_KEY"] = "like I'd tell you"
#app.config["USERNAME"] = "Eric"
#app.config["PASSWORD"] = "Schles"

from app import views, models