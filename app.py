from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % (os.path.join(basedir, 'db.sqlite'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Todo Class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), nullable=False)

# Todo Schema
class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'description', 'status')

# Init schema
todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)


@app.route('/api/list', methods=['GET'])
def index():
    # show all todos
    todo_list = Todo.query.all()
    result = todos_schema.dump(todo_list)
    
    return render_template("index.html" , todo_list=jsonify(result))


@app.route('/api/add', methods=['POST'])
def add():
    # add a new item
    desc = request.form.get("itemDescription").strip()

    if desc != "":
        new_todo = Todo(description= desc, status="Doing")
        db.session.add(new_todo)
        db.session.commit()

    return redirect(url_for("index"))


@app.route('/api/update', methods=['GET'])
def update():
    # edit an existing item
    itemID = request.args.get("id")
    desc = request.args.get("itemDescription").strip()
    itemStatus = request.args.get("itemStatus")
    
    if desc != "":
        todo = Todo.query.filter_by(id= itemID).first()
    
        if itemStatus == "Doing":
            todo.description = desc
            todo.status = "Done"
            db.session.commit()    
        else:
            todo.description = desc
            db.session.commit()

    return redirect(url_for("index"))
    

@app.route('/api/delete', methods=['GET'])
def delete():
    # remove an item
    itemID = request.args.get("id")

    todo = Todo.query.filter_by(id= itemID).first()
    db.session.delete(todo)
    db.session.commit()
    
    return redirect(url_for("index"))

# Start Server
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)