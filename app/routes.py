from flask import render_template

from app import app


@app.route('/hello')
def index():
    user = {'username': 'Marek'}
    return render_template('index.html', title='Shopping list', user=user)
