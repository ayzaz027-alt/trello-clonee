from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

# ---------------- DATABASE MODELS ----------------

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Todo')
    attachment = db.Column(db.String(200))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

# Create DB
with app.app_context():
    db.create_all()

# ---------------- ROUTES ----------------

@app.route('/')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@app.route('/add_project', methods=['POST'])
def add_project():
    name = request.form['name']
    desc = request.form['description']
    db.session.add(Project(name=name, description=desc))
    db.session.commit()
    return redirect(url_for('projects'))

@app.route('/project/<int:id>')
def tasks(id):
    project = Project.query.get_or_404(id)
    tasks = Task.query.filter_by(project_id=id).all()
    return render_template('tasks.html', project=project, tasks=tasks)

@app.route('/add_task/<int:id>', methods=['POST'])
def add_task(id):
    title = request.form['title']
    desc = request.form['description']
    file = request.files['file']

    filename = None
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    task = Task(
        title=title,
        description=desc,
        project_id=id,
        attachment=filename
    )
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('tasks', id=id))

# -------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
