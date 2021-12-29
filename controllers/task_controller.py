from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from models.todo  import db, Todo


def display_current_tasks(template):
    tasks = Todo.query.order_by(Todo.date_created).all()
    print(tasks)
    return render_template(template, tasks=tasks)

def display_task(id, template):
    task = Todo.query.get_or_404(id)
    return render_template(template, task=task)

def store(task_content):
    new_task = Todo(content=task_content)
    try:
        db.session.add(new_task)
        db.session.commit()
        return True
    except:
        return False

def delete_task(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return True
    except:
        return False

def update_task(id, new_content):
    task = Todo.query.get_or_404(id)
    try:
        task.content = new_content
        db.session.commit()
        return True
    except:
        return False