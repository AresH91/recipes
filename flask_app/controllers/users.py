from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
from flask import flash

bcrypt = Bcrypt(app)

# Index Login Route
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')


@app.route('/dashboard')
def dash():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    recipes = Recipe.get_all()
    return render_template('dashboard.html', info=User.show_one_user(data), recipes=recipes)


# Action Routes
# registration
@app.route('/register', methods=['POST'])
def create():
    if request.form['which_form'] == 'register':
        valid = User.validate_register(request.form)
        if not valid:
            return redirect('/')
        else:
            pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'fname': request.form['fname'],
        'lname': request.form['lname'],
        'email': request.form['email'],
        'password': pw_hash
    }
    User.register(data)
    new_user = User.email_check(data)
    session['user_id'] = new_user.id
    flash("You have successfully registered!", "register")
    return redirect('/dashboard')
# login
@app.route('/login', methods=['POST'])
def login():
    if request.form['which_form'] == 'login':
        print(request.form)
        data = {
            'email': request.form['email']
            }
        user_in_db = User.email_check(data)
        if not user_in_db:
            flash("Invalid Email/Password", "login")
            return redirect('/')
        if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            flash("Invalid Email/Password", "login")
            return redirect('/')
        session['user_id'] = user_in_db.id
        session['user_name'] = user_in_db.first_name
        return redirect('/dashboard')
# logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')