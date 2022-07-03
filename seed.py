def serialize_artist_data(artist):
    """Serialize an artist SQLAlchemy obj to dictionary"""
    #This is done so that it can be converted to JSON for our API using the jsonify method
    serialized = {
        "id": artist['id'],
        "name": artist['name'],
        "bio": artist['bio'],
        "image": artist['image'],}

def serialize_artist_names(artist):
    """Serialize an artist SQLAlchemy obj to dictionary"""
    #This is done so that it can be converted to JSON for our API using the jsonify method
    serialized = {
        "id": artist['id'],
        "name": artist['name']
    }
    return serialized        

def serialize_song(song):
    """Serialize a song SQLAlchemy obj to dictionary"""
    return {
        "id": song.id,
        "title": song.title,
        "image": song.image,
        "release_date": song.release_date,
        "lyrics": song.lyrics
    }

def serialize_album(album):
    """Serialize a album SQLAlchemy obj to dictionary"""
    return {
    "id": album.id,
    "title": album.title,
    "image": album.image,
    "bio": album.bio,
    "release_date": album.release_date
    }
