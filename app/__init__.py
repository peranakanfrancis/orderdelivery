"""
============================
This is the main home page
============================
"""
from flask import Flask

# Create Instance of Class
app = Flask(__name__)

app.config["DATABASE"] = 'losquatroamigos.db'
app.config['DEBUG'] = True



from app import models
from app.models import views
