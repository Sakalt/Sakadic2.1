from flask import Flask, request, jsonify
from models import db, DictionaryEntry, Translation, Content, Variation, Relation
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dictionary.db'
db.init_app(app)

@app.route('/entries', methods=['GET'])
def get_entries():
    entries = DictionaryEntry.query.all()
    return jsonify([entry.to_dict() for entry in entries])

@app.route('/entries', methods=['POST'])
def add_entry():
    data = request.json
    new_entry = DictionaryEntry(form=data['form'])
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(new_entry.to_dict()), 201

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        return jsonify(get_settings())
    elif request.method == 'POST':
        data = request.json
        update_settings(data)
        return jsonify(success=True)

@app.route('/export', methods=['GET'])
def export_json():
    data = {"words": [entry.to_dict() for entry in DictionaryEntry.query.all()], "version": 2}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
