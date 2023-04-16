from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


health_experts = Blueprint('health_experts', __name__)

# Get all nutritional advice posts from the DB
@health_experts.route('/nutritionaladviceposts', methods=['GET'])
def get_posts():
    cursor = db.get_db().cursor()
    cursor.execute('select n.title, h.first_name,\
        h.last_name from NutritionalAdvice n join healthexpert h on n.author_id = h.expert_id')
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
    current_app.logger.info(data)

    # extracting the variables
    title = data['post_title']
    body = data['post_body']

    # constructing the query
    query = 'insert into products (title, text_body) values("'
    query += title + '", "'
    query += body + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success!"

# Return a list of all nutritional advice posts from a particular health expert
@health_experts.route('/nutritionaladviceposts/<author_id>', methods=['GET'])
def get_author_posts(author_id):
    return "TODO"

# Return all the detailed information for a particular nutritional advice post
# including their title, text body, author, and timestamp
@health_experts.route('/nutritionaladviceposts/<author_id>/<post_id>', methods=['GET'])
def get_specific_post(author_id, post_id):
    return "TODO"

# Update the text body of the post from an expert
@health_experts.route('/nutritionaladviceposts/<author_id>/<post_id>', methods=['PUT'])
def update_post_body(author_id, post_id):
    return "TODO"

# Remove a nutritional advice post
@health_experts.route('/nutritionaladviceposts/<author_id>/<post_id>', methods=['DELETE'])
def remove_post(author_id, post_id):
    return "TODO"

# Expert recommends a new recipe
@health_experts.route('/recommendedrecipes/<expert_id>/<recipe_id>', methods=['POST'])
def recommend_recipe(expert_id, recipe_id):
    return "TODO"

# Expert unrecommends a recipe by removing it from their recommended list
@health_experts.route('/recommendedrecipes/<expert_id>/<recipe_id>', methods=['DELETE'])
def unrecommend_recipe(expert_id, recipe_id):
    return "TODO"

# Expert recommends a new meal plan for a specific user
@health_experts.route('/mealplans/<expert_id>/<user_id>', method=['POST'])
def recommend_meal_plan(expert_id, user_id):
    return "TODO"

# Expert unrecommends a user's meal plan from their list of recommended meal plans
@health_experts.route('/mealplans/<user_id>/<meal_plan_id>', method=['DELETE'])
def unrecommend_meal_plan(user_id, meal_plan_id):
    return "TODO"