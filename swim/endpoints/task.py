"""CRUD actions for tasks."""

from flask import g, Blueprint, request, redirect, render_template, url_for
from flask.ext.login import current_user, login_required

from swim import models
from swim import db
from swim.config import config


task_blueprint = Blueprint('task',
                           __name__,
                           url_prefix='%s/task' % config.get('url', 'base'))


@login_required
@task_blueprint.route('/', methods=['GET'])
def render_all_tasks_page():
    """Render all tasks.
    """
    tasks = db.session.query(models.Task)\
        .filter(models.Task.user_fk == current_user.id)\
        .filter(models.Task.status == 'done')\
        .order_by(models.Task.date_.desc())
    actions = models.Task.update_actions()
    return render_template('tasks_completed.html', tasks=tasks, actions=actions)


@login_required
@task_blueprint.route('/create', methods=['GET'])
def render_create_tasks_page():
    """Render create tasks page.
    """
    return render_template('tasks_create.html')


@login_required
@task_blueprint.route('/create', methods=['POST'])
def create_task():
    """Create new task.
    """
    description = request.form.get('description')
    if not description:
        return redirect(url_for('task.create_task'))
    task = models.Task(description, current_user)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index.render_index_page'))


@login_required
@task_blueprint.route('/update', methods=['POST'])
def update_tasks_via_form():
    """Update tasks when user selects checkboxes and submits form.
    """
    status = request.form.get('status')
    ids = [int(x) for x in request.form if x.isdigit()]
    tasks = [db.session.query(models.Task).get(id_) for id_ in ids]

    if status == 'deleted':
        for task in tasks:
            db.session.delete(task)
        db.session.commit()
    else:
        for task in tasks:
            task.status = status
            db.session.merge(task)
        db.session.commit()

    if '/task' in request.referrer:
        url = url_for('task.render_all_tasks_page')
    else:
        url = url_for('index.render_index_page')
    return redirect(url)


@login_required
@task_blueprint.route('/update_rank', methods=['POST'])
def update_tasks_via_js():
    """Update task when user reorders by dragging.
    """
    for update in request.json.get('updates'):
        task = db.session.query(models.Task).get(update['id'])
        task.rank = update['rank']
        task.status = update['status']
        db.session.merge(task)
    db.session.commit()
    return 'success'
