"""CRUD actions for tasks."""

import datetime
from flask import jsonify, Blueprint, request, redirect, render_template, url_for
from flask.ext.login import current_user, login_required

from swim import models, db, dbutils
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
        .order_by(models.Task.date_completed.desc())\
        .all()
    total_hours_spent = _get_hours(tasks)
    labels = db.session.query(models.Label)\
        .all()
    pct_time_per_label = {l.name: round(((_get_hours(l.tasks) / total_hours_spent) * 100), 2)
                          for l in labels}
    label_task_counts = {l.name: len(l.tasks) for l in labels}
    actions = models.Task.update_actions()
    total_tasks_completed = len(tasks)
    return render_template('tasks_completed.html', tasks=tasks,
                           actions=actions,
                           label_task_counts=label_task_counts,
                           total_tasks_completed=total_tasks_completed,
                           total_hours_spent=total_hours_spent,
                           pct_time_per_label=pct_time_per_label)


@login_required
@task_blueprint.route('/create', methods=['GET'])
def render_create_tasks_page():
    """Render create tasks page.
    """
    labels = db.session.query(models.Label).all()
    return render_template('tasks_create.html', labels=labels)


@login_required
@task_blueprint.route('/create', methods=['POST'])
def create_task():
    """Create new task.
    """
    description = request.form.get('description')
    if not description:
        return redirect(url_for('task.create_task'))
    duration = request.form.get('duration')
    # Default to 30 minutes per task.
    duration = int(duration) if duration else None
    labels = _get_or_create_labels(request.form.get('labels'))
    task = models.Task(description, current_user, duration, labels)
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
            task = _update_date_completed(task)
            db.session.merge(task)
        db.session.commit()

    if '/task' in request.referrer:
        url = url_for('task.render_all_tasks_page')
    else:
        url = url_for('index.render_index_page')
    return redirect(url)


@login_required
@task_blueprint.route('/update_via_json', methods=['POST'])
def update_tasks_via_js():
    """Update task when user reorders by dragging.
    """
    for update in request.json.get('updates'):
        task = db.session.query(models.Task).get(update['id'])

        duration = update['duration']
        # isdigit is perfect for our uses. It does not allow negative numbers
        # or decimals.
        if not duration.isdigit():
            msg = {'message': 'The duration must be an integer'}
            response = jsonify(msg)
            response.status_code = 415  # Error code 415 is for unsupported media.
            return response

        task.labels = _get_or_create_labels(update['labels'])

        task.duration = duration
        task.rank = update['rank']
        status = update['status']
        task.status = status
        task = _update_date_completed(task)
        task.description = update['description']

        db.session.merge(task)
    db.session.commit()
    return 'success'


def _get_hours(tasks):
    """Return total time in hours from list of tasks.
    """
    mins = sum([t.duration if t.duration else 0 for t in tasks])
    hours = mins / 60.0
    return round(hours, 2)


def _update_date_completed(task):
    """Return task with date_completed field properly assigned.
    """
    if task.status == 'done':
        if not task.date_completed:
            task.date_completed = datetime.datetime.utcnow().date()
    else:
        # Strip date_completed in case this is a task that was previously
        # considered completed but no longer is.
        task.date_completed = None
    return task


def _get_or_create_labels(label_names):
    """Get or create labels from HTTP request."""
    labels = []
    if not label_names or label_names == '' or not label_names:
        return labels
    for l in label_names.split(','):
        label = dbutils.get_or_create(models.Label, name=l.strip())
        labels.append(label)
    return labels
