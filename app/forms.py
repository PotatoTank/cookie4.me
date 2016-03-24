from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField('openif', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class AddCookie(Form):
    post = StringField('post')

