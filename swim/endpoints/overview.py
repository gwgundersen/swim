"""Render landing page."""

import json
from flask import Blueprint, render_template
from flask.ext.login import login_required
from sqlalchemy import text
import datetime

from swim import db, models
from swim.config import config


BASE_URL = config.get('url', 'base')
overview_blueprint = Blueprint('overview',
                            __name__,
                            url_prefix='%s/overview' % BASE_URL)


@overview_blueprint.route('/', methods=['GET'])
@login_required
def render_overview_page():
    """Render index page.
    """
    tasks = db.session.query(models.Task).all()
    labels = db.session.query(models.Label).all()

    # d1 = datetime.date(2016, 11, 03)
    d1 = datetime.date(2017, 6, 8)
    d2 = datetime.datetime.now().date()
    delta = d2 - d1
    days = []
    series_by_label = {l.name: [] for l in labels}

    for l in labels:
        for i in range(delta.days + 1):
            day = d1 + datetime.timedelta(days=i)
            days.append(str(day))
            total = _get_tasks_by_day(tasks, day, l.name)
            series_by_label[l.name].append(total)

    series = []
    for label_name, data in series_by_label.items():
        series.append({
            'name': label_name,
            'data': data
        })
    print(days)
    return render_template('overview.html',
                           series=json.dumps(series),
                           days=json.dumps(days))


def _get_tasks_by_day(tasks, day, label):
    """
    """
    total = 0
    for t in tasks:
        if not t.labels or t.labels[0].name != label:
            continue
        if t.date_completed != day:
            continue
        total += t.duration
    return total / 60.0