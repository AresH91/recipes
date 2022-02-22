from signal import alarm
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route('/recipes/<int:num>')
def show_recipe(num):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': num
    }
    return render_template('show_recipe.html', info=Recipe.get_Recipe(data))

@app.route('/recipes/new')
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('add_recipe.html')

@app.route('/recipes/edit/<int:num>')
def edit_recipe(num):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': num
    }
    info=Recipe.get_Recipe(data)
    if session['user_id'] != info.users_id:
        return redirect('/dashboard')
    return render_template('edit_recipe.html', info=info)

@app.route('/recipes/delete/<int:num>')
def delete_recipe(num):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': num
    }
    info=Recipe.get_Recipe(data)
    if session['user_id'] != info.users_id:
        return redirect('/dashboard')
    Recipe.delete_recipe(data)
    return redirect('/dashboard')

# action route
@app.route('/recipes/create', methods=['POST'])
def add_recipe():
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'made_on': request.form['made_on'],
        'under_30': request.form['under_30'],
        'users_id': session['user_id']
    }
    if not Recipe.validate_new_recipe(data):
        return redirect('/recipes/new')
    Recipe.create_recipe(data)
    return redirect('/dashboard')

@app.route('/recipes/edit/submit', methods=['POST'])
def update_recipe():
    num = request.form['id']
    data = {
        'id': request.form['id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'made_on': request.form['made_on'],
        'under_30': request.form['under_30']
    }
    if not Recipe.validate_new_recipe(data):
        return redirect(f'/recipes/edit/{num}')
    Recipe.update_recipe(data)
    return redirect('/dashboard')


