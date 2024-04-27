import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, template_folder="templates")
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

def init_session():
    if 'todos' not in session:
        session['todos'] = [{"task": "Sample TODO", "done": False}]

@app.route('/')
def index():
    init_session()
    todos = session['todos']
    return render_template("index.html", todos=todos)

@app.route("/add", methods=["POST"])
def add():
    init_session()
    todo = request.form['todo']
    session['todos'].append({"task": todo, "done": False})
    session.modified = True  # Mark session as modified
    return redirect(url_for("index"))


@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    init_session()
    todos = session['todos']
    todo = todos[index]
    if request.method == "POST":
        todo['task'] = request.form["todo"]
        session.modified = True  # Mark session as modified
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", todo=todo, index=index)

@app.route("/check/<int:index>", methods=["POST"])
def check(index):
    init_session()
    todos = session['todos']
    todos[index]['done'] = not todos[index]['done']
    session.modified = True  # Mark session as modified
    return redirect(url_for("index"))

@app.route("/delete/<int:index>")
def delete(index):
    init_session()
    todos = session['todos']
    del todos[index]
    session.modified = True  # Mark session as modified
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
