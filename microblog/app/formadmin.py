from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField
from wtforms.validators import DataRequired

class dbent(Form):
    tablename = TextField('tablename', validators = [DataRequired()])
    quess = TextField('quess', validators = [DataRequired()])
    answ = TextAreaField('answ', validators = [DataRequired()])
