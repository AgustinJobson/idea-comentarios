from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class getForm(FlaskForm):
    url1 = StringField(validators=[DataRequired()])
    url2 = StringField(validators=[DataRequired()])
