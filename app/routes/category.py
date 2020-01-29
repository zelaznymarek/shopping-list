from app import app


@app.route('/categories/<category_id>', methods=['GET'])
def get_one(category_id):
    return f'get category {category_id}'


@app.route('/categories', methods=['GET'])
def get_all():
    return 'get all categores'


@app.route('/categories', methods=['POST'])
def post():
    return 'post category'


@app.route('/categories/<category_id>', methods=['DELETE'])
def delete(category_id):
    return f'delete category {category_id}'
