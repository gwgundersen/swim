"""Represent a small win."""

import datetime
from sqlalchemy.sql import func

from swim import db


class Task(db.Model):

    __tablename__ = 'task'

    id          = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    status      = db.Column(db.String(255))
    date_       = db.Column(db.Date)
    user_fk     = db.Column(db.Integer, db.ForeignKey('user.id'),
                            nullable=True)
    rank        = db.Column(db.Integer)

    user = db.relationship('User', backref='tasks')

    def __init__(self, description, user):
        """Create a new small win."""
        self.description = description
        self.user = user
        self.date_ = datetime.datetime.now()
        self.status = 'todo'

        max_ = db.session.query(func.max(Task.rank)).one()[0]
        # Place element at bottom of to-do list.
        self.rank = max_ + 1

    @classmethod
    def update_actions(cls):
        """Canonical list of valid statuses for user interface components.
        """
        return ['todo', 'done', 'queued', 'deleted']
