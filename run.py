from app import app
import os
app.secret_key = os.urandom(12)
app.run(debug=True)
