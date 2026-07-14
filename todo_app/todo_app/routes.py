from flask import Blueprint, render_template, request, redirect, url_for
from models import Task
from storage import load_tasks, save_tasks, get_next_id

app = Blueprint('app', __name__)

@app.route("/")
def index():
    """
    Главная страница: отображает список всех задач.
    """
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    """
    Добавляет новую задачу.
    Получает заголовок из формы, создаёт задачу со статусом False,
    сохраняет в JSON и перенаправляет на главную.
    """
    title = request.form.get("title", "").strip()
    if title:
        tasks = load_tasks()
        new_id = get_next_id(tasks)
        tasks.append(Task(id=new_id, title=title, done=False))
        save_tasks(tasks)
    return redirect(url_for("app.index"))

@app.route("/done/<int:task_id>")
def mark_done(task_id):
    """
    Отмечает задачу как выполненную.
    Находит задачу по ID, меняет её статус на True и сохраняет.
    """
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.done = True
            break
    save_tasks(tasks)
    return redirect(url_for("app.index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    """
    Удаляет задачу по ID.
    Формирует новый список без задачи с указанным ID и сохраняет.
    """
    tasks = load_tasks()
    tasks = [task for task in tasks if task.id != task_id]
    save_tasks(tasks)
    return redirect(url_for("app.index"))

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    """
    Редактирует текст задачи.
    GET – показывает форму с текущим текстом.
    POST – принимает новый текст, обновляет задачу и сохраняет.
    """
    tasks = load_tasks()
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        return redirect(url_for("app.index"))
    if request.method == "POST":
        new_title = request.form.get("title", "").strip()
        if new_title:
            task.title = new_title
            save_tasks(tasks)
        return redirect(url_for("app.index"))
    return render_template("edit.html", task=task)
