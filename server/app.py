from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from database import init_db, db
from models import User, Dictionary, DictionaryEntry
from utils import generate_sentence, save_sentence, load_example_sentences

app = Flask(__name__, static_url_path='/Sakadic2.1')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dictionary.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.template_folder = "."

init_db(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('ユーザー名は既に存在します')
            return redirect(url_for('register'))
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('ユーザー名またはパスワードが無効です')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    dictionaries = Dictionary.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', dictionaries=dictionaries)

@app.route('/create_dictionary', methods=['POST'])
@login_required
def create_dictionary():
    name = request.form['name']
    new_dictionary = Dictionary(user_id=current_user.id, name=name)
    db.session.add(new_dictionary)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('Sakadic2.1//user/<username>/dict/<int:dictionary_id>')
@login_required
def view_dictionary(username, dictionary_id):
    dictionary = Dictionary.query.get_or_404(dictionary_id)
    if dictionary.user_id != current_user.id:
        return redirect(url_for('home'))
    return render_template('dictionary.html', dictionary=dictionary)

@app.route('/user/<username>/dict/<int:dictionary_id>/entries', methods=['GET'])
@login_required
def get_entries(username, dictionary_id):
    dictionary = Dictionary.query.get_or_404(dictionary_id)
    if dictionary.user_id != current_user.id:
        return redirect(url_for('home'))
    entries = DictionaryEntry.query.filter_by(dictionary_id=dictionary_id).all()
    return jsonify([entry.to_dict() for entry in entries])

@app.route('/user/<username>/dict/<int:dictionary_id>/entries', methods=['POST'])
@login_required
def add_entry(username, dictionary_id):
    dictionary = Dictionary.query.get_or_404(dictionary_id)
    if dictionary.user_id != current_user.id:
        return redirect(url_for('home'))
    data = request.json
    new_entry = DictionaryEntry(dictionary_id=dictionary_id, form=data['form'])
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(new_entry.to_dict()), 201

@app.route('/example_sentences', methods=['GET'])
@login_required
def example_sentences():
    sentences = load_example_sentences()
    return jsonify(sentences)

@app.route('/user/<username>/dict/<int:dictionary_id>/export', methods=['GET'])
@login_required
def export_json(username, dictionary_id):
    dictionary = Dictionary.query.get_or_404(dictionary_id)
    if dictionary.user_id != current_user.id:
        return redirect(url_for('home'))
    data = {"words": [entry.to_dict() for entry in DictionaryEntry.query.filter_by(dictionary_id=dictionary_id).all()], "version": 2}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
