"""Represent a many-to-many relationship between labels and tasks."""

from swim import db


labels = db.Column('label_fk', db.Integer, db.ForeignKey('label.id'))
tasks = db.Column('task_fk', db.Integer, db.ForeignKey('task.id'))
label_to_task = db.Table('label_to_task', db.metadata, labels, tasks)
