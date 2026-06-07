from flask import Flask, render_template, request, redirect, url_for
from models import Task
from storage import load_tasks, save_tasks, get_next_id

app = Flask(__name__)

# Убираем предупреждение ngrok (если используется)
@app.after_request
def add_ngrok_header(response):
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    if title:
        tasks = load_tasks()
        new_id = get_next_id(tasks)
        tasks.append(Task(id=new_id, title=title, done=False))
        save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/done/<int:task_id>")
def mark_done(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.done = True
            break
    save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task.id != task_id]
    save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        return redirect(url_for("index"))
    if request.method == "POST":
        new_title = request.form.get("title", "").strip()
        if new_title:
            task.title = new_title
            save_tasks(tasks)
        return redirect(url_for("index"))
    return render_template("edit.html", task=task)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
