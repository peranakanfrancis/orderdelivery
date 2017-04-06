from flask import Flask, render_template  # import class
app = Flask(__name__)  # create instance of class

app.config["DATABASE"] = 'losquatroamigos.db'
app.config['DEBUG'] = True

# don't know what this stuff is for.
# app.config["SECRET_KEY"] = "like I'd tell you"
# app.config["USERNAME"] = "Eric"
# app.config["PASSWORD"] = "Schles"

# Chin - commented out the bottom
# from app import views, models

@app.route("/")  # tells Flask what URL should trigger our function
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()