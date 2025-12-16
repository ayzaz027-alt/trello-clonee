from flask import Flask, render_template, request, redirect, jsonify
from models import db, Project, BoardList, Card

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

with app.app_context():
    db.create_all()

# ---------------- PROJECTS ----------------
@app.route('/')
def projects():
    return render_template('projects.html', projects=Project.query.all())

@app.route('/add_project', methods=['POST'])
def add_project():
    p = Project(name=request.form['name'])
    db.session.add(p)
    db.session.commit()

    for i, name in enumerate(['Todo', 'Doing', 'Done']):
        db.session.add(BoardList(name=name, project_id=p.id, position=i))
    db.session.commit()

    return redirect('/')

# ---------------- BOARD ----------------
@app.route('/project/<int:id>')
def board(id):
    lists = BoardList.query.filter_by(project_id=id).order_by(BoardList.position).all()
    cards = Card.query.all()
    return render_template('board.html', lists=lists, cards=cards, project_id=id)

@app.route('/add_card', methods=['POST'])
def add_card():
    card = Card(
        title=request.form['title'],
        list_id=request.form['list_id'],
        position=0
    )
    db.session.add(card)
    db.session.commit()
    return redirect(request.referrer)

# ---------------- DRAG DROP API ----------------
@app.route('/move_card', methods=['POST'])
def move_card():
    data = request.json
    card = Card.query.get(data['card_id'])
    card.list_id = data['list_id']
    db.session.commit()
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
