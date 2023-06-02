import billboard
import os
from flask import Flask, render_template, request, redirect
from forms import LandingPageForm, AddUserForm, LoginForm

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

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

@app.route('/', methods=["GET", "POST"])
def landing():
    """Landing page"""

    form = LandingPageForm()

    return render_template('/index.html', form=form)

@app.route('/getSong', methods=["GET", "POST"])
def getSong():
    """get the song and redirect back to landing page"""


    return redirect('/index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    """Landing page"""

    form = LoginForm()

    return render_template('/login.html', form=form)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Landing page"""

    form = AddUserForm()

    return render_template('/signup.html', form=form)