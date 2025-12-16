from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class BoardList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    position = db.Column(db.Integer)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    position = db.Column(db.Integer)
    list_id = db.Column(db.Integer, db.ForeignKey('board_list.id'))
