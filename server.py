from flask_app import app
from flask_app.controllers import recipes
from flask_app.controllers import users

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
