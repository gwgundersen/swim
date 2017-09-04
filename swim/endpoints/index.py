"""Render landing page."""

from datetime import date
from flask import Blueprint, render_template
from flask.ext.login import login_required
from sqlalchemy import cast, Date, or_

from swim import db, models, nytime
from swim.config import config


index_blueprint = Blueprint('index',
                            __name__,
                            url_prefix=config.get('url', 'base'))


@index_blueprint.route('/', methods=['GET'])
@login_required
def render_index_page():
    """Render index page.
    """
    not_upcoming = or_(
        models.Task.start_date == None,
        cast(models.Task.start_date, Date) <= date.today()
    )

    todo = db.session.query(models.Task)\
        .filter_by(status='todo')\
        .filter(not_upcoming)\
        .order_by(models.Task.rank)\
        .all()

    queued = db.session.query(models.Task)\
        .filter_by(status='queued')\
        .filter(not_upcoming)\
        .order_by(models.Task.rank)\
        .all()

    done = db.session.query(models.Task)\
        .filter(models.Task.status == 'done')\
        .filter(not_upcoming)\
        .filter(models.Task.date_completed == nytime.get_current_date())\
        .order_by(models.Task.rank)\
        .all()

    return render_template('index.html', todo=todo, queued=queued, done=done)
