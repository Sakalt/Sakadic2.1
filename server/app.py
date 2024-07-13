from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import db, User, DictionaryEntry, load_example_sentences
from utils import generate_sentence, save_sentence

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dictionary.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

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
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('ユーザー名またはパスワードが無効です')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/entries', methods=['GET'])
@login_required
def get_entries():
    entries = DictionaryEntry.query.filter_by(user_id=current_user.id).all()
    return jsonify([entry.to_dict() for entry in entries])

@app.route('/entries', methods=['POST'])
@login_required
def add_entry():
    data = request.json
    new_entry = DictionaryEntry(user_id=current_user.id, form=data['form'])
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(new_entry.to_dict()), 201

@app.route('/example_sentences', methods=['GET'])
@login_required
def example_sentences():
    sentences = load_example_sentences()
    return jsonify(sentences)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'GET':
        return jsonify(get_settings())
    elif request.method == 'POST':
        data = request.json
        update_settings(data)
        return jsonify(success=True)

@app.route('/export', methods=['GET'])
@login_required
def export_json():
    data = {"words": [entry.to_dict() for entry in DictionaryEntry.query.filter_by(user_id=current_user.id).all()], "version": 2}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
