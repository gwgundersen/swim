"""CRUD actions for Win objects."""

from flask import g, Blueprint, request, redirect, render_template, url_for
from flask.ext.login import current_user, login_required

from swimming import models
from swimming import db
from swimming.config import config


win_blueprint = Blueprint('win',
                          __name__,
                          url_prefix='%s/win' % config.get('url', 'base'))


@login_required
@win_blueprint.route('/', methods=['GET'])
def render_all_wins_page():
    """Render all wins.
    """
    wins = db.session.query(models.Win)\
        .filter(models.Win.user_fk == current_user.id)\
        .filter(models.Win.status == 'done')\
        .order_by(models.Win.date_.desc())
    actions = models.Win.update_actions()
    return render_template('wins_completed.html', wins=wins, actions=actions)


@login_required
@win_blueprint.route('/create', methods=['GET'])
def render_create_wins_page():
    """Render create wins page.
    """
    return render_template('wins_create.html')


@login_required
@win_blueprint.route('/create', methods=['POST'])
def create_win():
    """Create new win.
    """
    task = request.form.get('task')
    if not task:
        return redirect(url_for('win.create_win'))
    win = models.Win(task, current_user)
    db.session.add(win)
    db.session.commit()
    return redirect(url_for('index.render_index_page'))


@login_required
@win_blueprint.route('/update', methods=['POST'])
def update_wins_via_form():
    """Update wins when user selects checkboxes and submits form.
    """
    status = request.form.get('status')
    ids = [int(x) for x in request.form if x.isdigit()]
    wins = [db.session.query(models.Win).get(id_) for id_ in ids]

    if status == 'deleted':
        for win in wins:
            db.session.delete(win)
        db.session.commit()
    else:
        for win in wins:
            win.status = status
            db.session.merge(win)
        db.session.commit()

    if '/win' in request.referrer:
        url = url_for('win.render_all_wins_page')
    else:
        url = url_for('index.render_index_page')
    return redirect(url)


@login_required
@win_blueprint.route('/update_rank', methods=['POST'])
def update_wins_via_js():
    """Update win rank when user reorders by dragging.
    """
    for update in request.json.get('updates'):
        win = db.session.query(models.Win).get(update['id'])
        win.rank = update['rank']
        win.status = update['status']
        db.session.merge(win)
    db.session.commit()
    return 'success'
