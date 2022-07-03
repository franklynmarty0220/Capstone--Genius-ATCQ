""" SqlAlchemy models for Capstone"""


from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

########################################################################

class Songs(db.Model):
    """ List of All Songs of ATCQ
    
     this will be the center connect to other tables"""

    __tablename__ = 'songs'

    songs_id = db.Column(db.Integer,
            primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable = False)
    image = db.Column(db.String, nullable = False)
    lyrics = db.Column(db.String)

    #Chaining Artist to Songs
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.artist_id'))
    artist = db.relationship('Artist', secondary='Albums', backref='Songs')

    #Chaining Albums to Songs
    album_id = db.Column(db.Integer, db.ForeignKey('albums.album_id'))
    album = db.relationship('Albums', secondary = 'Artist', backref='Songs')

    #More info about the record
    release_date = db.Column(db.String)

    def __repr__(self):
        return f"<ID:{self/id}, Title:{self.title}"

class Albums(db.Model):
    """ Table of All Albums of ATCQ
        This will be linked to the Songs that Belong to the Albums"""
    
    __tablename__='albums'

    album_id = db.Column(db.Integer, primary_key=True)
    album_name = db.Column(db.String, nullable=False)
    bio = db.Column(db.String)
    image = db.Column(db.Text)

    

class Artist(db.Model):
    """ Table of the Artist ATCQ"""

    __tablename__='artist'

    artist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    bio = db.Column(db.String)
    image = db.Column(db.Text)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.Text, nullable=False,  unique=True)

    password = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False


