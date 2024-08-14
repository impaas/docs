from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Get database connection from environment variables
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg://{os.getenv('PGUSER')}:{os.getenv('PGPASSWORD')}@{os.getenv('PGHOST')}:{os.getenv('PGPORT')}/{os.getenv('PGDATABASE')}"
)

app.config["SQLALCHEMY_POOL_RECYCLE"] = 300

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form["task"]
        new_task = Todo(task=task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for("index"))
        except:
            return "There was an issue adding your task"
    else:
        tasks = Todo.query.order_by(Todo.id).all()
        return render_template("index.html", tasks=tasks)


@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    task = Todo.query.get_or_404(id)

    task.task = request.form["task"]
    try:
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "There was a problem updating the task"


@app.route("/complete/<int:id>", methods=["POST"])
def complete(id):
    task = Todo.query.get_or_404(id)

    try:
        task.complete = not task.complete
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "There was a problem toggling the task"


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    task = Todo.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "There was a problem deleting the task"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False, port=os.environ.get("PORT", 5000), host="0.0.0.0")
