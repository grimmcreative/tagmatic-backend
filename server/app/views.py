from flask import g
from flask.ext import restful

from app.server import api, db, flask_bcrypt, auth
from app.models import User, Post, ToDo, Contact, Project
from app.forms import UserCreateForm, SessionCreateForm, PostCreateForm, ToDoCreateForm, ToDoCompleteForm, \
    ContactCreateForm, ContactUpdateForm, ProjectCreateForm, ProjectUpdateForm
from app.serializers import UserSerializer, PostSerializer, ToDoSerializer, ContactSerializer, ProjectSerializer


@auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.user = user
    return flask_bcrypt.check_password_hash(user.password, password)


class UserView(restful.Resource):
    def post(self):
        form = UserCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422

        user = User(form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        return UserSerializer(user).data


class SessionView(restful.Resource):
    def post(self):
        form = SessionCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422

        user = User.query.filter_by(email=form.email.data).first()
        if user and flask_bcrypt.check_password_hash(user.password, form.password.data):
            return UserSerializer(user).data, 201
        return '', 401


class PostListView(restful.Resource):
    def get(self):
        posts = Post.query.all()
        return PostSerializer(posts, many=True).data

    @auth.login_required
    def post(self):
        form = PostCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        post = Post(form.title.data, form.body.data)
        db.session.add(post)
        db.session.commit()
        return PostSerializer(post).data, 201


class PostView(restful.Resource):
    def get(self, id):
        posts = Post.query.filter_by(id=id).first()
        return PostSerializer(posts).data


class ToDoListView(restful.Resource):
    def get(self):
        todos = ToDo.query.all()
        return ToDoSerializer(todos, many=True).data

    def post(self):
        form = ToDoCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        todo = ToDo(form.text.data, form.is_complete.data, 'Active')
        db.session.add(todo)
        db.session.commit()
        return ToDoSerializer(todo).data, 201

    def delete(self):
        toDelete = ToDo.query.filter(ToDo.is_complete == True).all()
        for todo in toDelete:
            db.session.delete(todo)
        db.session.commit()
        todos = ToDo.query.all()
        return ToDoSerializer(todos, many=True).data, 201


class ToDoView(restful.Resource):
    def get(self, id):
        todos = ToDo.query.filter_by(id=id).first()
        return ToDoSerializer(todos).data

    def put(self, id):
        form = ToDoCompleteForm()
        if not form.validate_on_submit():
            return form.errors, 422
        todo = ToDo.query.filter_by(id=id).first()
        todo.is_complete = form.is_complete.data
        if todo.is_complete:
            todo.status = 'Completed'
        else:
            todo.status = 'Active'
        db.session.commit()
        return ToDoSerializer(todo).data, 201


class ContactListView(restful.Resource):
    def get(self):
        contacts = Contact.query.all()
        return ContactSerializer(contacts, many=True).data

    def post(self):
        form = ContactCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        contact = Contact(form.text.data, form.first_name.data, form.last_name.data, form.is_selected.data)
        db.session.add(contact)
        db.session.commit()
        return ContactSerializer(contact).data, 201

    def delete(self):
        toDelete = Contact.query.filter(Contact.is_selected == True).all()
        for contact in toDelete:
            db.session.delete(contact)
        db.session.commit()
        contacts = Contact.query.all()
        return ContactSerializer(contacts, many=True).data, 201


class ContactView(restful.Resource):
    def get(self, id):
        contacts = Contact.query.filter_by(id=id).first()
        return ContactSerializer(contacts).data

    def put(self, id):
        form = ContactUpdateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        contact = Contact.query.filter_by(id=id).first()
        contact.first_name = form.first_name.data
        contact.last_name = form.last_name.data
        contact.text = form.text.data
        db.session.commit()
        return ContactSerializer(contact).data, 201

    def delete(self, id):
        contact = Contact.query.filter_by(id=id).first()
        db.session.delete(contact)
        db.session.commit()
        contacts = Contact.query.all()
        return ContactSerializer(contacts, many=True).data


class ProjectListView(restful.Resource):
    def get(self):
        projects = Project.query.all()
        return ProjectSerializer(projects, many=True).data

    def post(self):
        form = ProjectCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        project = Project(form.description.data, form.user.data)
        db.session.add(project)
        db.session.commit()
        return ProjectSerializer(project).data, 201


api.add_resource(UserView, '/api/v1/users')
api.add_resource(SessionView, '/api/v1/sessions')
api.add_resource(PostListView, '/api/v1/posts')
api.add_resource(PostView, '/api/v1/posts/<int:id>')
api.add_resource(ToDoListView, '/api/v1/todos')
api.add_resource(ToDoView, '/api/v1/todos/<int:id>')
api.add_resource(ContactListView, '/api/v1/contacts')
api.add_resource(ContactView, '/api/v1/contacts/<int:id>')
api.add_resource(ProjectListView, '/api/v1/projects')
