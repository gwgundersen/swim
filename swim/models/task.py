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
    date_completed = db.Column(db.Date)
    user_fk        = db.Column(db.Integer, db.ForeignKey('user.id'),
                               nullable=True)
    rank           = db.Column(db.Integer)
    duration       = db.Column(db.Integer)

    user = db.relationship('User', backref='tasks')
    labels = db.relationship('Label', secondary='label_to_task')

    def __init__(self, description, user, duration, labels):
        """Create a new small win."""
        self.description = description
        self.user = user
        self.date_created = datetime.datetime.now()
        self.status = 'todo'

        max_ = db.session.query(func.max(Task.rank)).one()[0]
        # Place element at bottom of to-do list.
        self.rank = max_ + 1
        self.duration = duration
        self.labels = labels

    @classmethod
    def update_actions(cls):
        """Canonical list of valid statuses for user interface components.
        """
        return ['todo', 'done', 'queued', 'deleted']
