from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    name = StringField('Category name', validators=[DataRequired])
    submit = SubmitField('Add category')


class ListForm(FlaskForm):
    products = [StringField(f'name_{i}') for i in range(20)]
    submit = SubmitField('Add list')
