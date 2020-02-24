from flask import Blueprint, jsonify, make_response, request, current_app
from sqlalchemy.orm.exc import NoResultFound


from app.models import Category
from app.errors import UserInputException

categories = Blueprint('categories', __name__)


@categories.route('/categories/<category_id>', methods=['GET'])
def get_one(category_id):
    id = validate_id(category_id)

    try:
        category = Category.query.filter(Category.id == id).one()
    except NoResultFound:
        return make_response(f'Category with id {id} not found', 404)

    return make_response(jsonify(category), 200)


@categories.route('/categories', methods=['GET'])
def get_all():
    return 'get all categories'


@categories.route('/categories', methods=['POST'])
def post():
    try:
        name = request.json['name']
    except KeyError:
        raise UserInputException(f'Validation error: `name` parameter is required.')

    category = Category(name=name)
    print(category)

    current_app.db.sesssion.add(category)
    current_app.db.session.commit()

    return make_response(jsonify(category), 200)


@categories.route('/categories/<category_id>', methods=['DELETE'])
def delete(category_id):
    return f'delete category {category_id}'


def validate_id(category_id):
    try:
        return int(category_id)
    except ValueError:
        raise UserInputException(f'Validation error: `category_id` should be an int.')


def respond(msg, code):
    headers = {'Content-Type': 'application/json'}
    response = make_response(msg, code)
    response.headers = headers

    return response
