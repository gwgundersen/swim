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
    if range_arg == 'all':
        # The first task in the database is on 2016-11-03 but I didn't start
        # using Swim regularly until 2017-06-08.
        d1 = datetime.date(2017, 6, 8)
        d2 = datetime.datetime.now().date()
    else:
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
            year, month, day = _get_most_recent_start_of_week()
            d1 = datetime.date(year, month, day)
            d2 = d1 + datetime.timedelta(6)

    stackedSeries, days, pieSeries, stats = _get_all_data(d1, d2)
    return render_template('report.html',
                           stackedSeries=json.dumps(stackedSeries),
                           days=json.dumps(days),
                           pieSeries=json.dumps(pieSeries),
                           stats=stats)

@report_blueprint.route('/everyday', methods=['GET'])
@login_required
def render_everyday_report():
    DAYS_IN_YEAR = 365
    now          = datetime.datetime.now()
    start        = datetime.date(now.year, 01, 01)
    next_year    = datetime.date(now.year+1, 01, 01)
    days_so_far  = (now.date() - start).days
    days_left    = DAYS_IN_YEAR - days_so_far

    tasks = db.session.query(models.Task)\
        .join(models.label_to_task)\
        .join(models.Label)\
        .filter_by(name='ka_math')\
        .filter(models.Task.date_completed >= start)\
        .filter(models.Task.date_completed < next_year)\
        .distinct()

    total_mins      = sum([t.duration for t in tasks])
    total_hrs       = round(total_mins / 60.0)
    hours_behind    = days_so_far - total_hrs
    if hours_behind <= 0:
        catchup_min_day = 0
    else:
        catchup_min_day = round((hours_behind * 60) / days_left, 1)

    return render_template('everyday.html',
                           total_hrs=total_hrs,
                           days_so_far=days_so_far,
                           hours_behind=hours_behind,
                           catchup_min_day=catchup_min_day)


def _get_all_data(date1, date2):
    """Return data for tasks within the range between date1 and date2.
    """
    tasks = db.session.query(models.Task).all()
    labels = db.session.query(models.Label).all()
    delta = date2 - date1

    days = []
    series_by_label = {l.name: [] for l in labels}
    label_subtotals = {}
    for l in labels:
        label_subtotals[l.name] = 0
        for i in range(delta.days + 1):
            day = date1 + datetime.timedelta(days=i)
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

    # This is the format that Highcharts.js requires.
    stackedSeries = []
    for label_name, data in series_by_label.items():
        stackedSeries.append({
            'name': label_name,
            'data': data
        })

    pieSeries = []
    for label_name, data in label_subtotals.items():
        if data == 0:
            continue
        pieSeries.append({
            'name': label_name,
            'y': data
        })

    total_hrs = sum(hrs_per_day)
    hrs_day = total_hrs / delta.days
    stats = {
        'total_hrs': total_hrs,
        'hrs_day': hrs_day,
        'median_hrs': _median(hrs_per_day),
        'label_subtotals': label_subtotals
    }

    return stackedSeries, days, pieSeries, stats


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


def _get_most_recent_start_of_week():
    """Return the year, month, and day of the most recent beginning of the
    week, i.e. the most recent Monday.
    """
    today = datetime.date.today()
    mon = today - datetime.timedelta(days=today.weekday())
    return mon.year, mon.month, mon.day
