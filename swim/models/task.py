"""Represent a small win."""

import datetime
from sqlalchemy.sql import func

from swim import db


class Task(db.Model):

    __tablename__ = 'task'

    id             = db.Column(db.Integer, primary_key=True)
    description    = db.Column(db.String(255))
    status         = db.Column(db.String(255))
    date_created   = db.Column(db.Date)
    start_date     = db.Column(db.DateTime)
    date_completed = db.Column(db.Date)
    user_fk        = db.Column(db.Integer, db.ForeignKey('user.id'),
                               nullable=True)
    rank           = db.Column(db.Integer)
    duration       = db.Column(db.Integer)

    user = db.relationship('User', backref='tasks')
    labels = db.relationship('Label', backref='tasks', secondary='label_to_task')

    def __init__(self, description, user, duration, start_date, labels):
        """Create a new small win."""
        self.description = description
        self.user = user
        self.date_created = datetime.datetime.now()
        self.start_date = start_date
        self.status = 'queued'

        max_ = db.session.query(func.max(Task.rank)).one()[0]
        # Place element at bottom of to-do list.
        self.rank = max_ + 1
        self.duration = duration
        self.labels = labels

    @property
    def labels_as_string(self):
        """Return labels formatted as a comma-separated list for viewing.
        """
        if len(self.labels) == 0:
            return ''
        return ', '.join([l.name for l in self.labels])

    @property
    def start_date_human_readable(self):
        if not self.start_date:
            return ''
        return self.start_date.strftime('%B %d (%A) at %I:%M %p')

    @property
    def start_date_string(self):
        if not self.start_date:
            return ''
        return self.start_date.strftime('%Y-%m-%d %H:%M')

    @property
    def days_until(self):
        if not self.start_date:
            return ''
        now = datetime.datetime.now()
        until = (self.start_date.date() - now.date()).days
        return until if until > 0 else 0

    @property
    def duration_in_hours(self):
        return round(self.duration / 60, 2)

    @property
    def is_reminder(self):
        return self.start_date is not None
