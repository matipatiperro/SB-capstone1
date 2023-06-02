from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class LandingPageForm(FlaskForm):
    """Form on the landing page"""

    date = StringField('date:', validators=[DataRequired()], description="yyyy-mm-dd or yyyy")
    chartType = StringField('chart:', validators=[DataRequired()], description="default top-100")
    image_url = StringField('(Optional) Image URL', description="test") 

class AddUserForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()],description="desired username")
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)], description="at least 6 digits")

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()], description="your username")
    password = PasswordField('Password', validators=[Length(min=6)], description="your password")