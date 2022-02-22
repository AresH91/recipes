from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.config.mysqlconnection import MySQLConnection

from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.made_on = data['made_on']
        self.under_30 = data['under_30']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, made_on, under_30, users_id, created_at, updated_at) VALUES ( %(name)s, %(description)s, %(instructions)s, %(made_on)s, %(under_30)s, %(users_id)s, NOW(), NOW())"
        return connectToMySQL('Recipes').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes"
        results = connectToMySQL('Recipes').query_db(query)
        recipes = []
        if not results:
            return recipes
        else:
            for num in results:
                recipes.append(cls(num))
        print(recipes)
        return recipes

    @classmethod
    def get_Recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        results = connectToMySQL('Recipes').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE Recipes.recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, made_on = %(made_on)s, under_30 = %(under_30)s, updated_at = NOW() where id = %(id)s;"
        return connectToMySQL('Recipes').query_db(query, data)

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE from recipes where id = %(id)s"
        return connectToMySQL('Recipes').query_db(query, data)

# Static Methods
    @staticmethod
    def validate_new_recipe(data):
        print(data['made_on'])
        is_valid = True
        if len(data['name']) < 3:
            flash("Recipe name must be 3 or more characters!", "new_rec")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description must be 3 or more characters!", "new_rec")
            is_valid = False
        if len(data['instructions']) < 3:
            flash("Instructions must be 3 or more characters!", "new_rec")
            is_valid = False
        return is_valid