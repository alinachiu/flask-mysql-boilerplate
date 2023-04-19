from flask import Blueprint, request, jsonify, make_response
import json
from src import db


users = Blueprint('users', __name__)

# Return a list of all nutritional advice posts from a particular health expert
@users.route('/nutritionaladviceposts/<author_id>', methods=['GET'])
def get_author_posts(author_id):
    cursor = db.get_db().cursor()
    cursor.execute('select n.title, h.first_name,\
        h.last_name from NutritionalAdvice n join HealthExpert h on n.author_id = h.expert_id\
                   where n.author_id =' + str(author_id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Return a filtered list of recipes that people with dietary restriction can eat
@users.route('/recipesrestriction/<restriction_id>', methods=['GET'])
def get_restriction_recipe(restriction_id):
    cursor = db.get_db().cursor()
    cursor.execute('select name, description, preparation_time, cooking_time, serving_size, image_url, source_url,\
                   calories, carbohydrates, protein, fat, sodium, fiber, sugar \
                   from Recipe r join RecipeDietaryRestriction rdr on r.recipe_id = rdr.recipe_id \
                   where rdr.restriction_id = ' + str(restriction_id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(json.dumps(json_data, indent = 4, sort_keys = True, default = str))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Return a filtered list of recipes that include the ingredient
@users.route('/recipesingredient/<ingredient_id>', methods=['GET'])
def get_ingredient_recipe(ingredient_id):
    cursor = db.get_db().cursor()
    cursor.execute('select name, description, preparation_time, cooking_time, serving_size, image_url, source_url,\
                   calories, carbohydrates, protein, fat, sodium, fiber, sugar \
                   from Recipe r join RecipeIngredient ri on r.recipe_id = ri.recipe_id \
                   where ri.ingredient_id = ' + str(ingredient_id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(json.dumps(json_data, indent = 4, sort_keys = True, default = str))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Gets all meal plans from an expert for a user
@users.route('/mealplans/<expert_id>/<user_id>', methods=['GET'])
def get_meal_plans(expert_id, user_id):
    cursor = db.get_db().cursor()
    cursor.execute('select u.first_name as "User First Name", u.last_name as "User Last Name", h.first_name as "Expert First Name", h.last_name as "Expert Last Name", m.start_date, m.end_date from MealPlan m\
        join HealthExpert h on m.dietitian_id = h.expert_id join User u on m.user_id = u.user_id where m.dietitian_id = ' + str(expert_id) + ' and m.user_id = ' + str(user_id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Return all the detailed information for a user's personalized meal plan
@users.route('/mealplans/<meal_plan_id>', methods=['GET'])
def get_meal_plan(meal_plan_id):
    cursor = db.get_db().cursor()
    cursor.execute('select u.first_name as user_first_name, u.last_name as user_last_name, h.first_name as expert_first_name, h.last_name as expert_last_name, m.start_date, m.end_date, u.user_id, m.meal_plan_id from MealPlan m\
        join HealthExpert h on m.dietitian_id = h.expert_id join User u on m.user_id = u.user_id where m.meal_plan_id = ' + str(meal_plan_id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# User updates a meal plan from a list of recommended meal plans
@users.route('/mealplans/<meal_plan_id>', methods=['PUT'])
def update_meal_plan(meal_plan_id):
    # collecting data from the request object
    data = request.json

    # extracting the text body
    start_date = data['new_start_date']
    end_date = data['new_end_date']

    # constructing the query
    query = 'update MealPlan set start_date = "'
    query += start_date + '", end_date = "'
    query += end_date + '" where meal_plan_id = '
    query += meal_plan_id

    # executing and committing the update statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"

# User deletes a meal plan from a list of recommended meal plans
@users.route('/mealplans/<meal_plan_id>', methods=['DELETE'])
def delete_meal_plan(meal_plan_id):
    # constructing the query
    query = 'delete from MealPlan where meal_plan_id = ' + meal_plan_id

    # executing and committing the delete statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"

# Return a list of all a user’s user goals
@users.route('/usergoals/<user_id>', methods=['GET'])
def get_all_user_goals(user_id):
    cursor = db.get_db().cursor()
    cursor.execute('select ug.goal_id, g.goal_name from UserGoal ug join Goal g \
                   on ug.goal_id = g.goal_id where ug.user_id = ' + str(user_id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Generate a new user goal for the user
@users.route('/usergoals/<user_id>', methods=['POST'])
def add_new_goal(user_id):
    # collecting data from the request object
    data = request.json

    # extracting the variables
    goal = data['goal_id']

    # constructing the query
    query = 'insert into UserGoal (user_id, goal_id) values('
    query += user_id + ', '
    query += str(goal) + ')'

    # executing and committing the insert statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"

# Return all the detailed information for a particular user goal
@users.route('/usergoals/<user_id>/<goal_id>', methods=['GET'])
def get_user_goal(user_id, goal_id):
    cursor = db.get_db().cursor()
    cursor.execute('select g.goal_name, u.first_name, u.last_name from UserGoal ug join Goal g \
                   on ug.goal_id = g.goal_id join User u on ug.user_id = u.user_id \
                    where ug.user_id = ' + str(user_id) + ' and ug.goal_id = ' + str(goal_id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Delete a user's specific goal
@users.route('/usergoals/<user_id>/<goal_id>', methods=['DELETE'])
def delete_user_goal(user_id, goal_id):
    # constructing the query
    query = 'delete from UserGoal where user_id = ' + \
        user_id + ' and goal_id = ' + goal_id

    # executing and committing the delete statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"