from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField('openif', validators=[DataRequired()], render_kw={"placeholder": "Email or OpenID"})
    rfid_tag = StringField('rfid tag', render_kw={"placeholder": "RFID Tag (first time only)"})
    remember_me = BooleanField('remember_me', default=False)

class AddCookie(Form):
    post = StringField('post')

