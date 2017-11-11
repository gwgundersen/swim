"""Render landing page."""

from calendar import monthrange
import json
from flask import request, Blueprint, render_template
from flask.ext.login import login_required
import datetime

from swim import db, models
from swim.config import config


BASE_URL = config.get('url', 'base')
report_blueprint = Blueprint('report',
                             __name__,
                             url_prefix='%s/report' % BASE_URL)


@report_blueprint.route('/', methods=['GET'])
@login_required
def render_report():
    """Render index page.
    """
    range_arg = request.args.get('range')
    parts = range_arg.split('.') if range_arg else []
    if len(parts) == 2:
        year = int(parts[0])
        month = int(parts[1])
        r = monthrange(year, month)
        d1 = datetime.date(year, month, 1)
        d2 = d1 + datetime.timedelta(r[1])
    elif len(parts) == 3:
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        d1 = datetime.date(year, month, day)
        d2 = d1 + datetime.timedelta(6)
    else:
        # The first task in the database is:
        #
        #    d1 = datetime.date(2016, 11, 03)
        #
        # But I did not actually Swim regularly using it until:
        d1 = datetime.date(2017, 6, 8)
        d2 = datetime.datetime.now().date()

    # I'm interested in:
    #     Total hours work in period.
    #     Percent per label.
    #     Avg. hour per day.
    series, days, report = _get_all_data(d1, d2)
    return render_template('report.html',
                           series=json.dumps(series),
                           days=json.dumps(days),
                           report=report)


def _get_all_data(d1, d2):
    """
    """
    tasks = db.session.query(models.Task).all()
    labels = db.session.query(models.Label).all()
    delta = d2 - d1
    days = []
    series_by_label = {l.name: [] for l in labels}

    label_subtotals = {}
    for l in labels:
        label_subtotals[l.name] = 0
        for i in range(delta.days + 1):
            day = d1 + datetime.timedelta(days=i)
            days.append(str(day))
            subtotal = _get_hours_per_task_per_day(tasks, day, l.name)
            series_by_label[l.name].append(subtotal)
            label_subtotals[l.name] += subtotal

    hrs_per_day = []
    for i in range(delta.days + 1):
        subtotal = 0
        for l in labels:
            subtotal += series_by_label[l.name][i]
        hrs_per_day.append(subtotal)

    series = []
    for label_name, data in series_by_label.items():
        series.append({
            'name': label_name,
            'data': data
        })

    total_hrs = sum(hrs_per_day)
    hrs_day = total_hrs / delta.days
    report = {
        'total_hrs': round(total_hrs, 1),
        'hrs_day': round(hrs_day, 1),
        'median_hrs': _median(hrs_per_day),
        'label_subtotals': label_subtotals
    }
    return series, days, report


def _get_hours_per_task_per_day(tasks, day, label):
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


def _median(lst):
    """Returns median of list.
    """
    lst = sorted(lst)
    length = len(lst)
    if length % 2 == 0:
        idx = (length / 2)
        two = lst[idx-1:idx+1]
        return sum(two) / 2
    else:
        idx = (length / 2) + 1
        return lst[idx]
