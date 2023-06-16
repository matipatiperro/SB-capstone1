import billboard
import os
from flask import Flask, render_template, request, redirect, flash, session, g, request
from forms import LandingPageForm, AddUserForm, LoginForm, PlaylistForm, SongForm
from models import db, connect_db, User, Playlist, Song
from sqlalchemy.exc import IntegrityError

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///capstone1'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

# needed once to create the tables within the db
# with app.app_context():
#     db.drop_all()
#     db.create_all()


# Use the ChartData constructor to download a chart:

# ChartData(name, date=None, year=None, fetch=True, timeout=25)
# The arguments are:

# name – The chart name, e.g. 'hot-100' or 'pop-songs'.
# date – The chart date as a string, in YYYY-MM-DD format. By default, the latest chart is fetched.
# year – The chart year, if requesting a year-end chart. Must be a string in YYYY format. Cannot supply both date and year.
# fetch – A boolean indicating whether to fetch the chart data from Billboard.com immediately (at instantiation time). If False, the chart data can be populated at a later time using the fetchEntries() method.
# max_retries – The max number of times to retry when requesting data (default: 5).
# timeout – The number of seconds to wait for a server response. If None, no timeout is applied.

# chart types https://www.billboard.com/charts/
#  hot-100, billboard-200, artist-100, streaming-songs, radio-songs, digital-song-sales, top-album-sales,
# billboard-u-s-afrobeats-songs, current-albums, catalog-albums, independent-albums, soundtracks, vinyl-albums

# charts/year-end/
# 2022/top-artists, 2022/top-artists-duo-group, 2022/top-artists-female, 2022/top-artists-male, 2022/top-new-artists, 2022/labels


# chart = billboard.ChartData('hot-100', date='1981-08-20')
# print (chart)
# song = chart[0]  # Get no. 1 song on chart
# song.title + ' by ' + song.artist
# song.weeks  # Get no. of weeks on chart

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/', methods=["GET"])
def landing():
    """Landing page"""
    form = LandingPageForm()

    return render_template('/index.html', form=form)

@app.route('/artist-song', methods=["POST"])
def artistSong():
    """get the song and redirect back to landing page"""
    date = request.form["date"]
    chartType = request.form["chartType"] or "top-100"

    form = PlaylistForm()

    if(len(date)==4):
        chartType = "top-artists"
        chart = billboard.ChartData(chartType, year=date)
    else:
        chart = billboard.ChartData(chartType, date)
    # print (chart)
    result = chart[0]  # Get no. 1 song on chart

    # print(date, chartType)
    # flash(f"{date} and {chartType}")
    if CURR_USER_KEY in session:
        playlists = g.user.playlists
    else:
        playlists=None
    # flash(f"top result was {result} from {chartType} for date {date}")
    flash(result)
    return render_template('/billboardResponse.html', form=form, playlists=playlists)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Landing page"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = AddUserForm()

    if form.validate_on_submit():

        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """login page"""
    # print(session[CURR_USER_KEY])
    # print(User.query.get(session[CURR_USER_KEY]))
    # if CURR_USER_KEY in session:
    #     # already logged in
    #     flash("Already logged in.", 'danger')
    #     return redirect("/")

    form = LoginForm()

    if form.validate_on_submit():
        # returns user if success, returns false if fails
        user = User.authenticate(form.username.data,
                                 form.password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        if User.query.filter_by(username=form.username.data).first()==None:
            flash(f"Username {form.username.data} does not exist", 'danger')
        else:
            flash("Invalid username or credentials.", 'danger')

    # return redirect("/")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/")


####-------- playlist stuff
@app.route('/addplaylist', methods=["POST"])
def addPlaylist():
    """create playlist page"""
    if CURR_USER_KEY in session:
        # g.user = User.query.get(session[CURR_USER_KEY])
        form = PlaylistForm()

        playlist = Playlist(
                name=form.name.data,
                description=form.description.data,
            )

        db.session.add(playlist)
        db.session.commit()

        g.user.playlists.append(playlist)
        db.session.commit()

        # playlists = Playlist.query.all()
        # playlists = g.user.playlists
        
        return redirect(f"/user/{g.user.id}/playlists")
    else:
        # g.user = None
        return redirect('/login')

@app.route('/editplaylist/<int:playlist_id>', methods=["POST"])
def editPlaylist(playlist_id):
    """create playlist page"""
    if CURR_USER_KEY in session:
        # g.user = User.query.get(session[CURR_USER_KEY])
        form = PlaylistForm()
        playlist = Playlist.query.get_or_404(playlist_id)
        playlist.name=form.name.data
        playlist.description=form.description.data

        db.session.commit()

        # playlists = Playlist.query.all()
        # playlists = g.user.playlists
        
        return redirect(f"/user/{g.user.id}/playlists")
    else:
        # g.user = None
        return redirect('/login')

@app.route('/removeplaylist/<int:playlist_id>', methods=["POST"])
def removePlaylist(playlist_id):
    """delete playlist"""
    if CURR_USER_KEY in session:
        # g.user = User.query.get(session[CURR_USER_KEY])
        playlist = Playlist.query.get_or_404(playlist_id)
        
        db.session.delete(playlist)
        db.session.commit()
        
        return redirect(f"/user/{g.user.id}/playlists")
    else:
        # g.user = None
        return redirect('/login')

@app.route('/user/<int:user_id>/playlists')
def playlists_show(user_id):
    """Show users playlists."""
    user = User.query.get_or_404(user_id)
    playlists = g.user.playlists
    # user = User.query.get_or_404(user_id)
    form = PlaylistForm()
    
    return render_template('/showUser.html', user=user, playlists=playlists, form=form)

@app.route('/user/<int:user_id>/playlist')
def create_playlist(user_id):
    """ create playlist."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
        form = PlaylistForm()
        return render_template('/playlist.html', form=form, type="create")

    else:
        g.user = None
        return redirect('/login')

@app.route('/user/<int:user_id>/playlist/<int:playlist_id>/edit')
def edit_playlist(user_id, playlist_id):
    """Edit an existing playlist."""
    # user = User.query.get_or_404(user_id)
    playlist = Playlist.query.get_or_404(playlist_id)

    form = PlaylistForm()
    form.name.data = playlist.name
    form.description.data = playlist.description

    return render_template('/playlist.html', form=form,type="edit",playlist=playlist)


####-------- song stuff

@app.route('/user/<int:user_id>/playlist/<int:playlist_id>', methods=["GET","POST"])
def show_playlist(user_id, playlist_id):
    """Show user playlist or add song to playlist."""
    form = SongForm()
    user = User.query.get_or_404(user_id)
    playlist = Playlist.query.get_or_404(playlist_id)

    print(f"playlist id: {playlist_id}")

    if form.validate_on_submit():
    # if flask.request.method == 'POST':
        print(f"playlist id inside: {playlist_id}")
        # returns user if success, returns false if fails
        song = Song(
                artist=form.artist.data,
                title=form.title.data,
                notes=form.notes.data,
            )

        db.session.add(song)
        db.session.commit()

        playlist = Playlist.query.get(playlist_id)

        playlist.songs.append(song)
        db.session.commit()
        # songs = Song.query.all()
        songs = playlist.songs
        return redirect(f"/user/{user.id}/playlist/{playlist.id}")
    else:
        print(form.errors)
        flash("failed to valid.", 'danger')
        # songs = Song.query.all()
        songs = playlist.songs
    # user = User.query.get_or_404(user_id)
    
    return render_template('/showPlaylist.html', user=user, playlist=playlist, form=form, songs=songs)
