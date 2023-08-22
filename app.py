from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

# FangList
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25))
    content = db.Column(db.String(300))

    def __init__(self, title, content):
        self.title = title
        self.content = content

class NoteSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "content")

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)

#  Create Note
@app.route('/note', methods=['POST'])
def add_note():
    title = request.json['title']
    content = request.json['content']
    new_note = Note(title, content)
    db.session.add(new_note)
    db.session.commit()
    return note_schema.jsonify(new_note)

# Read Note
@app.route('/note', methods=['GET'])
def get_notes():
    all_notes = Note.query.all()
    result = notes_schema.dump(all_notes)
    return jsonify(result)

@app.route('/note/<id>', methods=['GET'])
def get_note(id):
    note = Note.query.get(id)
    result = note_schema.dump(note)
    return jsonify(result)

# Update Note
@app.route('/note/<id>', methods=['PUT'])
def update_note(id):
    note = Note.query.get(id)
    title = request.json['title']
    content = request.json['content']
    note.title = title
    note.content = content
    db.session.commit()
    return note_schema.jsonify(note)

# Delete Note
@app.route('/note/<id>', methods=['DELETE'])
def delete_note(id):
    note = Note.query.get(id)
    db.session.delete(note)
    db.session.commit()
    return note_schema.jsonify(note)

# Kickstart the App
if __name__ == '__main__':
    app.run(debug=True)