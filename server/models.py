from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DictionaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form = db.Column(db.String(80), unique=True, nullable=False)
    translations = db.relationship('Translation', backref='entry', lazy=True)
    tags = db.relationship('Tag', backref='entry', lazy=True)
    contents = db.relationship('Content', backref='entry', lazy=True)
    variations = db.relationship('Variation', backref='entry', lazy=True)
    relations = db.relationship('Relation', backref='entry', lazy=True)

    def to_dict(self):
        return {
            "entry": {"id": self.id, "form": self.form},
            "translations": [t.to_dict() for t in self.translations],
            "tags": [tag.text for tag in self.tags],
            "contents": [content.to_dict() for content in self.contents],
            "variations": [v.to_dict() for v in self.variations],
            "relations": [r.to_dict() for r in self.relations],
        }

class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    forms = db.Column(db.String(200))
    entry_id = db.Column(db.Integer, db.ForeignKey('dictionary_entry.id'), nullable=False)

    def to_dict(self):
        return {"title": self.title, "forms": self.forms.split(',')}

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80))
    entry_id = db.Column(db.Integer, db.ForeignKey('dictionary_entry.id'), nullable=False)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    text = db.Column(db.Text)
    markdown = db.Column(db.Text)
    entry_id = db.Column(db.Integer, db.ForeignKey('dictionary_entry.id'), nullable=False)

    def to_dict(self):
        return {"title": self.title, "text": self.text, "markdown": self.markdown}

class Variation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    form = db.Column(db.String(80))
    entry_id = db.Column(db.Integer, db.ForeignKey('dictionary_entry.id'), nullable=False)

    def to_dict(self):
        return {"title": self.title, "form": self.form}

class Relation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    entry_id = db.Column(db.Integer, db.ForeignKey('dictionary_entry.id'), nullable=False)
    related_entry_id = db.Column(db.Integer)

    def to_dict(self):
        related_entry = DictionaryEntry.query.get(self.related_entry_id)
        return {"title": self.title, "entry": {"id": related_entry.id, "form": related_entry.form}}
