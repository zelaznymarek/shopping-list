from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db/shopping'
app.config['DEBUG'] = True

db = SQLAlchemy()
db.init_app(app)


@app.route('/hello')
def hello():
    return 'hello'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
