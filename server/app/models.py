from flask import g

from wtforms.validators import Email

from app.server import db, flask_bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, info={'validators': Email()})
    password = db.Column(db.String(80), nullable=False)
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.password = flask_bcrypt.generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.email


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.user_id = g.user.id

    def __repr__(self):
        return '<Post %r>' % self.title


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    is_complete = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.String(120), nullable=False, default='Active')
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, text, is_complete, status):
        self.text = text
        self.is_complete = is_complete
        self.status = status

    def __repr__(self):
        return '<ToDo %r>' % self.text


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    text = db.Column(db.Text, nullable=False)
    icon_url = db.Column(db.String(120), nullable=True)
    is_selected = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, text, first_name, last_name, is_selected):
        self.text = text
        self.first_name = first_name
        self.last_name = last_name
        self.is_selected = is_selected

    def __repr__(self):
        return '<ToDo %r>' % self.text


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, description):
        self.description = description
        self.user_id = g.user.id

    def __repr__(self):
        return '<Project %r>' % self.description

