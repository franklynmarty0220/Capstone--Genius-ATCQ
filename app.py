#from lyricsgenius import Genius

#genius = Genius('3sZiCak0ojeSjlYxhkuu5rWrypbT5rhnK4m9Txwx4s6wQ5jqhBJSekZwd6Vcb2RL')
#artist = genius.search_artist('A Tribe Called Quest')
#song = artist.song("Scenario")
#print(song.lyrics)

from flask import Flask, render_template, redirect, session, flash, jsonify
from lyricsgenius import Genius
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Songs, Artist, Albums, User
from seed import serialize_artist_data,serialize_song, serialize_album
from forms import UserForm
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///atcq_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

db.create_all()

####### LYRICS ########

@app.route("/api/artists/<int:id>", methods = ["GET"])
def get_artist(id):
    """Return JSON for a specific artist in database"""
    artist = Artist.query.get(id)
    artist_dict = artist.__dict__
    serialized = serialize_artist_data(artist_dict)
    return serialized

@app.route("/api/artists/<int:artist_id>/<int:song_id>/lyrics")
def get_lyric_by_artist(artist_id, song_id):
    artist = Artist.query.get(artist_id)
    song = Songs.query.get(song_id)
    return song.lyrics

@app.route("/artists/<int:id>/albums")
def get_songs_by_artist(id):
    artist = Artist.query.get(id)
    serialized = [serialize_album(album) for album in artist.album]
    return jsonify(songs=serialized)

@app.route("/artists/<int:artist_id>/<int:song_id>")
def get_song_by_artist(song_id):
    song = Songs.query.get(song_id)
    serialized = serialize_song(song)
    return jsonify(songs=serialized)

@app.route("/artists/<int:id>/songs")
def get_songs_by_artist(id):
    artist = Artist.query.get(id)
    serialized = [serialize_song(song) for song in artist.songs]
    return jsonify(songs=serialized)


@app.route("/api/artists/<int:artist_id>/<int:song_id>/lyrics")
def get_lyric_by_artist(artist_id, song_id):
    artist = Artist.query.get(artist_id)
    song = Songs.query.get(song_id)
    return song.lyrics


######## LOGIN/ REGISTER #########

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.register(username, password)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        session['user_id'] = new_user.id
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/tweets')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['user_id'] = user.id
            return redirect('/tweets')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect('/')
