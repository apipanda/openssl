from flask_wtf import FlaskForm as Form
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Required


class SearchForm(Form):
    bvn = StringField("Enrollees BVN", validators=[Required()])
    submit = SubmitField('Submit')
