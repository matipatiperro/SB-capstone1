from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class LandingPageForm(FlaskForm):
    """Form on the landing page"""

    date = StringField('date:', validators=[DataRequired()], description="yyyy-mm-dd or yyyy")
    chartType = StringField('chart:', description="default top-100")

class AddUserForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()],description="desired username")
    password = PasswordField('Password', validators=[Length(min=5)], description="at least 5 digits")

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()], description="your username")
    password = PasswordField('Password', validators=[Length(min=6)], description="your password")

class PlaylistForm(FlaskForm):
    """create playlist form."""

    name = StringField('name of the playlist', validators=[DataRequired()], description="playlist name")
    description = StringField('playlist description', description="description of playlist")

class SongForm(FlaskForm):
    """create song for playlist form."""

    artist = StringField('artist', validators=[DataRequired()], description="artist name")
    title = StringField('song title', description="song title")
    notes = StringField('song notes', description="notes on the song")