from flask.ext.wtf import Form

from wtforms_alchemy import model_form_factory
from wtforms import StringField
from wtforms.validators import DataRequired

from app.server import db
from app.models import User, Post, ToDo

BaseModelForm = model_form_factory(Form)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class UserCreateForm(ModelForm):
    class Meta:
        model = User


class SessionCreateForm(Form):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


class PostCreateForm(ModelForm):
    class Meta:
        model = Post

class ToDoCreateForm(ModelForm):
    class Meta:
        model = ToDo