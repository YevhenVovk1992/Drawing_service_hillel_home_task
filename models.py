from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class TaskQueue(db.Model):
    __tablename__ = 'task_queue'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String, nullable=True, unique=True)
    status = db.Column(db.String, nullable=True, default='send to broker')
