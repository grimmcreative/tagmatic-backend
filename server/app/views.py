from flask import g
from flask.ext import restful

from app.server import api, db, flask_bcrypt, auth
from app.models import User, Post, ToDo, Contact, Project, Issue, Tag, Milestone, Effort, Column
from app.forms import UserCreateForm, SessionCreateForm, PostCreateForm, ToDoCreateForm, ToDoCompleteForm, \
    ContactCreateForm, ContactUpdateForm, ProjectCreateForm, ProjectUpdateForm, IssueCreateForm, TagCreateForm, MilestoneCreateForm, EffortCreateForm, ColumnCreateForm
from app.serializers import UserSerializer, PostSerializer, ToDoSerializer, ContactSerializer, ProjectSerializer, IssueSerializer, \
    TagSerializer, MilestoneSerializer, EffortSerializer, ColumnSerializer


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
        project = Project(form.name.data, form.description.data, form.user_id.data)
        db.session.add(project)
        db.session.commit()
        return ProjectSerializer(project).data, 201

class ProjectView(restful.Resource):
    def get(self, id):
        projects = Project.query.filter_by(id=id).first()
        return ProjectSerializer(projects).data

    def put(self, id):
        form = ProjectUpdateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        project = Project.query.filter_by(id=id).first()
        project.name = form.name.data
        project.description = form.description.data
        project.user_id = form.user_id.data
        db.session.commit()
        return ProjectSerializer(project).data, 201

    def delete(self, id):
        project = Project.query.filter_by(id=id).first()
        db.session.delete(project)
        db.session.commit()
        projects = Project.query.all()
        return ProjectSerializer(projects, many=True).data


class IssueListView(restful.Resource):
    def get(self):
        issues = Issue.query.all()
        return IssueSerializer(issues, many=True).data

    def post(self):
        form = IssueCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        issue = Issue(form.title.data, form.description.data, form.project_id.data, form.column_id.data,
                      form.tag_id.data, form.milestone_id.data, form.effort_id.data, form.assigned_to_id.data)
        db.session.add(issue)
        db.session.commit()
        return IssueSerializer(issue).data, 201


class IssueView(restful.Resource):
    def get(self, id):
        issues = Issue.query.filter_by(id=id).first()
        return IssueSerializer(issues).data

    def put(self, id):
        form = IssueCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        issue = Issue.query.filter_by(id=id).first()
        issue.title = form.title.data
        issue.description = form.description.data
        issue.project_id = form.project_id.data
        issue.column_id = form.column_id.data
        issue.tag_id = form.tag_id.data
        issue.milestone_id = form.milestone_id.data
        issue.effort_id = form.effort_id.data
        issue.assigned_to_id = form.assigned_to_id.data
        db.session.commit()
        return IssueSerializer(issue).data, 201

    def delete(self, id):
        issue = Issue.query.filter_by(id=id).first()
        db.session.delete(issue)
        db.session.commit()
        issues = Issue.query.all()
        return IssueSerializer(issues, many=True).data


class TagListView(restful.Resource):
    def get(self):
        tags = Tag.query.all()
        return TagSerializer(tags, many=True).data

    def post(self):
        form = TagCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        tag = Tag(form.name.data, form.description.data, form.color.data)
        db.session.add(tag)
        db.session.commit()
        return TagSerializer(tag).data, 201


class TagView(restful.Resource):
    def get(self, id):
        tags = Tag.query.filter_by(id=id).first()
        return TagSerializer(tags).data

    def put(self, id):
        form = TagCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        tag = Tag.query.filter_by(id=id).first()
        tag.name = form.name.data
        tag.description = form.description.data
        tag.color = form.color.data
        db.session.commit()
        return TagSerializer(tag).data, 201

    def delete(self, id):
        tag = Tag.query.filter_by(id=id).first()
        db.session.delete(tag)
        db.session.commit()
        tags = Tag.query.all()
        return TagSerializer(tags, many=True).data

class MilestoneView(restful.Resource):
    def get(self, id):
        milestones = Milestone.query.filter_by(id=id).first()
        return MilestoneSerializer(milestones).data

    def put(self, id):
        form = MilestoneCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        milestone = Milestone.query.filter_by(id=id).first()
        milestone.name = form.name.data
        milestone.description = form.description.data
        milestone.due_date = form.due_date.data
        milestone.stats = form.status.data
        db.session.commit()
        return MilestoneSerializer(milestone).data, 201

    def delete(self, id):
        milestone = Milestone.query.filter_by(id=id).first()
        db.session.delete(milestone)
        db.session.commit()
        milestones = Milestone.query.all()
        return MilestoneSerializer(milestones, many=True).data

class MilestoneListView(restful.Resource):
    def get(self):
        milestones = Milestone.query.all()
        return MilestoneSerializer(milestones, many=True).data

    def post(self):
        form = MilestoneCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        milestone = Milestone(form.name.data, form.description.data, form.due_date.data, form.status.data)
        db.session.add(milestone)
        db.session.commit()
        return MilestoneSerializer(milestone).data, 201

class EffortListView(restful.Resource):
    def get(self):
        efforts = Effort.query.all()
        return EffortSerializer(efforts, many=True).data

    def post(self):
        form = EffortCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        effort = Effort(form.name.data, form.description.data)
        db.session.add(effort)
        db.session.commit()
        return EffortSerializer(effort).data, 201

class EffortView(restful.Resource):
    def get(self, id):
        efforts = Effort.query.filter_by(id=id).first()
        return EffortSerializer(efforts).data

    def put(self, id):
        form = EffortCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        effort = Effort.query.filter_by(id=id).first()
        effort.name = form.name.data
        effort.description = form.description.data
        db.session.commit()
        return EffortSerializer(effort).data, 201

    def delete(self, id):
        effort = Effort.query.filter_by(id=id).first()
        db.session.delete(effort)
        db.session.commit()
        efforts = Effort.query.all()
        return TagSerializer(efforts, many=True).data

class ColumnListView(restful.Resource):
    def get(self):
        columns = Column.query.all()
        return ColumnSerializer(columns, many=True).data

    def post(self):
        form = ColumnCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        column = Column(form.name.data, form.description.data)
        column.tasks = []
        db.session.add(column)
        db.session.commit()
        return ColumnSerializer(column).data, 201

class ColumnView(restful.Resource):
    def get(self, id):
        column = Column.query.filter_by(id=id).first()
        return ColumnSerializer(column).data

    def put(self, id):
        form = ColumnCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        column = Column.query.filter_by(id=id).first()
        column.name = form.name.data
        column.description = form.description.data
        db.session.commit()
        return ColumnSerializer(column).data, 201

    def delete(self, id):
        column = Column.query.filter_by(id=id).first()
        db.session.delete(column)
        db.session.commit()
        columns = Column.query.all()
        return ColumnSerializer(columns, many=True).data

api.add_resource(UserView, '/api/v1/users')
api.add_resource(SessionView, '/api/v1/sessions')
api.add_resource(PostListView, '/api/v1/posts')
api.add_resource(PostView, '/api/v1/posts/<int:id>')
api.add_resource(ToDoListView, '/api/v1/todos')
api.add_resource(ToDoView, '/api/v1/todos/<int:id>')
api.add_resource(ContactListView, '/api/v1/contacts')
api.add_resource(ContactView, '/api/v1/contacts/<int:id>')
api.add_resource(ProjectListView, '/api/v1/projects')
api.add_resource(ProjectView, '/api/v1/projects/<int:id>')
api.add_resource(IssueListView, '/api/v1/issues')
api.add_resource(IssueView, '/api/v1/issues/<int:id>')
api.add_resource(TagListView, '/api/v1/tags')
api.add_resource(TagView, '/api/v1/tags/<int:id>')
api.add_resource(MilestoneListView, '/api/v1/milestones')
api.add_resource(MilestoneView, '/api/v1/milestones/<int:id>')
api.add_resource(EffortListView, '/api/v1/efforts')
api.add_resource(EffortView, '/api/v1/efforts/<int:id>')
api.add_resource(ColumnListView, '/api/v1/columns')
api.add_resource(ColumnView, '/api/v1/columns/<int:id>')