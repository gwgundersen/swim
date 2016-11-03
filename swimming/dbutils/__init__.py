"""Utility methods for managing the database."""

from swimming import db


def get_or_create(model, **kwargs):
    """Return instance if it exists, create it otherwise."""
    instance = db.session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance


def delete(model, id):
    """Deletes an instance if it exists."""
    instance = db.session.query(model).get(id)
    if instance:
        db.session.delete(instance)
