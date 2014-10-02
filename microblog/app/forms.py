from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import DataRequired
#from wtforms_alchemy import ModelForm

class LoginForm(Form):
    openid = TextField('openid', validators = [DataRequired()])