from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


health_experts = Blueprint('health_experts', __name__)

# Get all nutritional advice posts from the DB
@health_experts.route('/nutritionaladviceposts', methods=['GET'])
def get_posts():
    cursor = db.get_db().cursor()
    cursor.execute('select n.title, h.first_name,\
        h.last_name from NutritionalAdvice n join HealthExpert h on n.author_id = h.expert_id')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Create a new nutritional advice post
@health_experts.route('/nutritionaladviceposts', methods=['POST'])
def add_new_post():
    # collecting data from the request object
    data = request.json

    # extracting the variables
    title = data['post_title']
    body = data['post_body']
    author = data['author_id']

    # constructing the query
    query = 'insert into NutritionalAdvice (title, text_body, author_id) values("'
    query += title + '", "'
    query += body + '", '
    query += str(author) + ')'

    # executing and committing the insert statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"

# Return a list of all nutritional advice posts from a particular health expert
@health_experts.route('/nutritionaladviceposts/<author_id>', methods=['GET'])
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

# Return all the detailed information for a particular nutritional advice post
# including their title, text body, author name, and timestamp
@health_experts.route('/nutritionaladviceposts/<author_id>/<post_id>', methods=['GET'])
def get_specific_post(author_id, post_id):
    cursor = db.get_db().cursor()
    cursor.execute('select n.title, n.text_body, h.first_name, h.last_name, n.date_posted\
                   from NutritionalAdvice n join HealthExpert h on n.author_id = h.expert_id\
                   where n.post_id =' + str(post_id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Update the text body of the post from an expert
@health_experts.route('/nutritionaladviceposts/<author_id>/<post_id>', methods=['PUT'])
def update_post_body(author_id, post_id):
    # collecting data from the request object
    data = request.json

    # extracting the text body
    body = data['new_post_body']

    # constructing the query
    query = 'update NutritionalAdvice set text_body = "'
    query += body + '" where post_id = '
    query += post_id + ' and author_id = ' + author_id

    # executing and committing the update statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"

# Remove a nutritional advice post
@health_experts.route('/nutritionaladviceposts/<author_id>/<post_id>', methods=['DELETE'])
def remove_post(author_id, post_id):
    # constructing the query
    query = 'delete from NutritionalAdvice where post_id = ' + post_id + ' and author_id = ' + author_id

    # executing and committing the delete statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"

# Expert recommends a new meal plan for a specific user
@health_experts.route('/mealplans/<expert_id>/<user_id>', methods=['POST'])
def recommend_meal_plan(expert_id, user_id):
    # collecting data from the request object
    data = request.json

    # extracting the variables
    start_date = data['start_date']

    # constructing the query
    set_key_query = 'set @new_key := (SELECT meal_plan_id FROM MealPlan ORDER BY meal_plan_id DESC LIMIT 1)'
    select_key_query = 'select @new_key'
    query = 'insert into MealPlan (meal_plan_id, dietitian_id, user_id, start_date) values (@new_key + 1, '
    query += expert_id + ', '
    query += user_id + ', "'
    query += start_date + '")'

    # executing and committing the insert statement
    cursor = db.get_db().cursor()
    cursor.execute(set_key_query)
    cursor.execute(select_key_query)
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"

# Expert updates a user's meal plan in their list of recommended meal plans
@health_experts.route('/mealplans/<user_id>/<meal_plan_id>', methods=['PUT'])
def update_meal_plan(user_id, meal_plan_id):
    # collecting data from the request object
    data = request.json

    # extracting the text body
    start_date = data['new_start_date']

    # constructing the query
    query = 'update MealPlan set start_date = "'
    query += start_date + '" where user_id = '
    query += user_id + ' and meal_plan_id = ' + meal_plan_id

    # executing and committing the update statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"

# Expert unrecommends a user's meal plan from their list of recommended meal plans
@health_experts.route('/mealplans/<user_id>/<meal_plan_id>', methods=['DELETE'])
def unrecommend_meal_plan(user_id, meal_plan_id):
    # constructing the query
    query = 'delete from MealPlan where user_id = ' + user_id + ' and meal_plan_id = ' + meal_plan_id

    # executing and committing the delete statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"

# Gets all meal plans from an expert for a user
@health_experts.route('/mealplans/<expert_id>/<user_id>', methods=['GET'])
def get_meal_plans(expert_id, user_id):
    cursor = db.get_db().cursor()
    cursor.execute('select u.first_name as "User First Name", u.last_name as "User Last Name", h.first_name as "Expert First Name", h.last_name as "Expert Last Name", m.start_date, m.end_date from MealPlan m\
        join HealthExpert h on m.dietitian_id = h.expert_id join User u on m.user_id = u.user_id')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response