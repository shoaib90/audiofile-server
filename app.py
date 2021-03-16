from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, Schema
from marshmallow.validate import Length, Range
import os
import json
import datetime


# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Song Class/Model


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(100), unique=True)
    duration = db.Column(db.Integer)
    uploaded_time = db.Column(db.DateTime, auto_now_add=True)

    def __init__(self, song_name, duration, uploaded_time):
        self.song_name = song_name
        self.duration = duration
        self.uploaded_time = uploaded_time

# Podcast Class/Model


class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    podcast_name = db.Column(db.String(100), unique=True)
    duration = db.Column(db.Integer)
    uploaded_time = db.Column(db.DateTime, auto_now_add=True)
    host = db.Column(db.String(100))
    participants = db.Column(db.String())

    def __init__(self, podcast_name, duration, uploaded_time, host, participants):
        self.podcast_name = podcast_name
        self.duration = duration
        self.uploaded_time = uploaded_time
        self.host = host
        self.participants = participants

# AudioBook Class/Model


class Audiobook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    author = db.Column(db.String(100))
    narattor = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    uploaded_time = db.Column(db.DateTime, auto_now_add=True)

    def __init__(self, title, author, narattor, duration, uploaded_time):
        self.title = title
        self.author = author
        self.narattor = narattor
        self.duration = duration
        self.uploaded_time = uploaded_time

# Song Schema


class SongSchema(ma.Schema):

    id = fields.Int()
    song_name = fields.Str(required=True, validate=Length(max=100))
    duration = fields.Int(required=True)
    uploaded_time = fields.DateTime(required=True)

# Podcast Schema


class PodcastSchema(ma.Schema):

    id = fields.Int()
    podcast_name = fields.Str(required=True, validate=Length(max=100))
    duration = fields.Int(required=True)
    uploaded_time = fields.DateTime(required=True)
    host = fields.Str(required=True, validate=Length(max=100))
    participants = fields.List(fields.Str(
        validate=Length(max=100)), validate=Range(max=10))


# AudioBook Schema

class AudioBookSchema(ma.Schema):

    id = fields.Int()
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    narattor = fields.Str(required=True)
    duration = fields.Int(required=True)
    uploaded_time = fields.DateTime(required=True)


# Init schema
song_schema = SongSchema()
song_schemas = SongSchema(many=True)


audiobook_schema = AudioBookSchema()
audiobook_schemas = AudioBookSchema(many=True)

podcast_schema = PodcastSchema()
podcast_schemas = PodcastSchema(many=True)


@app.route('/audio/create', methods=['POST'])
def add_item():
    """
    This function takes 2 parameters audioFileType and audioFileMetaData
    and based on the data passed in the body it updates the db and add new 
    item in the table of a particular audioFileType.
    """
    try:
        # result = json.loads(request.data)
        if request.json["audioFileType"] == 'Song':
            song_name = request.json['audioFileMetadata']['song_name']
            duration = request.json['audioFileMetadata']['duration']
            uploaded_time = datetime.datetime.now()

            if not song_name or not duration:
                return jsonify(message="The request is invalid"), 400

            new_song = Song(song_name, duration, uploaded_time)

            db.session.add(new_song)
            db.session.commit()

            # return song_schema.jsonify(new_song)
            return jsonify(message="Action is successful"), 200

        elif request.json["audioFileType"] == 'Podcast':
            podcast_name = request.json['audioFileMetadata']['podcast_name']
            duration = request.json['audioFileMetadata']['duration']
            uploaded_time = datetime.datetime.now()
            host = request.json['audioFileMetadata']['host']
            participants = request.json['audioFileMetadata']['participants']

            if not podcast_name or not duration or not host:
                return jsonify(message="The request is invalid"), 400

            new_podcast = Podcast(podcast_name, duration,
                                  uploaded_time, host, participants)

            db.session.add(new_podcast)
            db.session.commit()

            return jsonify(message="Action is successful"), 200

        elif request.json["audioFileType"] == 'Audiobook':
            title = request.json['audioFileMetadata']['title']
            author = request.json['audioFileMetadata']['author']
            narattor = request.json['audioFileMetadata']['narattor']
            duration = request.json['audioFileMetadata']['duration']
            uploaded_time = datetime.datetime.now()

            if not title or not author or not narattor or not duration:
                return jsonify(message="The request is invalid"), 400

            new_audiobook = Audiobook(
                title, author, narattor, duration, uploaded_time)

            db.session.add(new_audiobook)
            db.session.commit()

            return jsonify(message="Action is successful"), 200

        else:
            return jsonify(message="The request is invalid"), 400
    except Exception as e:
        return jsonify(
            message=str(e),
        ), 500

# Get All Products


@app.route('/audio/<audioFileType>', methods=['GET'])
def get_products(audioFileType):
    """
    This function takes the audioFileType and return the list of audio data of that type.
    """
    try:
        if audioFileType == "Song":
            all_audio_files = Song.query.all()
            result = song_schemas.dump(all_audio_files)
            return jsonify(message="Action is Successful", data=result.data), 200

        elif audioFileType == "Podcast":
            all_audio_files = Podcast.query.all()
            result = podcast_schemas.dump(all_audio_files)
            return jsonify(message="Action is Successful", data=result.data), 200
        elif audioFileType == "Audiobook":
            all_audio_files = Audiobook.query.all()
            result = audiobook_schemas.dump(all_audio_files)
            return jsonify(message="Action is Successful", data=result.data), 200
        else:
            return jsonify(message="The request is invalid"), 400
    except Exception as e:
        return jsonify(
            message=str(e),
        ), 500

    # return result

# Get Single Audio


@app.route('/audio/<audioFileType>/<audioFileID>', methods=['GET'])
def get_product(audioFileType, audioFileID):
    """
    This function takes the audioFileType and audioFileID and return the particular audio data of that ID.
    """
    try:
        if audioFileType == "Song":
            song = Song.query.get(audioFileID)
            # data = song_schema.song
            return song_schema.jsonify(song), 200
        elif audioFileType == "Podcast":
            podcast = Podcast.query.get(audioFileID)
            return podcast_schema.jsonify(podcast), 200
        elif audioFileType == "Audiobook":
            audiobook = Audiobook.query.get(audioFileID)
            return audiobook_schema.jsonify(audiobook), 200
        else:
            return jsonify(message="The request is invalid"), 400
    except Exception as e:
        return jsonify(
            message=str(e),
        ), 500

# Update a Product


@app.route('/audio/<audioFileType>/<audioFileID>', methods=['PUT'])
def update_product(audioFileType, audioFileID):
    """
    This function updates the existing records based on the audioFileType and audioFileID provided.
    """
    try:

        if audioFileType == "Song":
            song = Song.query.get(audioFileID)

            song_name = request.json['audioFileMetadata']['song_name']
            duration = request.json['audioFileMetadata']['duration']
            uploaded_time = datetime.datetime.now()

            if not song_name or not duration:
                return jsonify(message="The request is invalid"), 400

            song.song_name = song_name
            song.duration = duration
            song.uploaded_time = uploaded_time

            db.session.commit()

            return song_schema.jsonify(song), 200

        elif audioFileType == "Podcast":
            podcast = Podcast.query.get(audioFileID)

            podcast_name = request.json['podcast_name']
            duration = request.json['duration']
            uploaded_time = datetime.datetime.now()
            host = request.json['host']
            participants = request.json['participants']

            if not podcast_name or not duration or not host:
                return jsonify(message="The request is invalid"), 400

            podcast.podcast_name = podcast_name
            podcast.duration = duration
            podcast.uploaded_time = uploaded_time
            podcast.host = host
            podcast.participants = participants

            db.session.commit()

            return podcast_schema.jsonify(podcast), 200
        elif audioFileType == "Audiobook":
            audiobook = Audiobook.query.get(audioFileID)

            title = request.json['title']
            author = request.json['author']
            narattor = request.json['narattor']
            duration = request.json['duration']
            uploaded_time = datetime.datetime.now()

            if not title or not author or not narattor or not duration:
                return jsonify(message="The request is invalid"), 400

            audiobook.title = title
            audiobook.author = author
            audiobook.narattor = narattor
            audiobook.duration = duration
            audiobook.uploaded_time = uploaded_time

            db.session.commit()

            return audiobook_schema.jsonify(audiobook), 200
        else:
            return jsonify(message="The request is invalid"), 400
    except Exception as e:
        return jsonify(
            message=str(e),
        ), 500

# Delete Product


@app.route('/audio/<audioFileType>/<audioFileID>', methods=['DELETE'])
def delete_product(audioFileType, audioFileID):
    """
    This function deletes the existing audio file present in the db, based on the audioFileType and audioFileID provided. 
    """
    try:
        if audioFileType == "Song":
            song = Song.query.get(audioFileID)
            db.session.delete(song)
            db.session.commit()
            return song_schema.jsonify(song)
        elif audioFileType == "Podcast":
            podcast = Podcast.query.get(audioFileID)
            db.session.delete(podcast)
            db.session.commit()
            return podcast_schema.jsonify(podcast)
        elif audioFileType == "Audiobook":
            audiobook = Audiobook.query.get(audioFileID)
            db.session.delete(audiobook)
            db.session.commit()
            return audiobook_schema.jsonify(audiobook)
        else:
            return jsonify(message="The request is invalid"), 400
    except Exception as e:
        return jsonify(
            message=str(e),
        ), 500


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
