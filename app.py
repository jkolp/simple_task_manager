from flask import Flask, render_template, url_for, request, redirect
from models.todo import db, Todo
from controllers.task_controller import display_current_tasks, display_task, store, delete_task, update_task

app = Flask(__name__) # __name__ is reference to the file name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

# Index page and Create tasks route
@app.route('/', methods=['POST', 'GET']) # this route can receive post and get
def index():
    if request.method == 'GET':
        return display_current_tasks('index.html')
    else:
        # POST request will attempt storing task, if success redirect('/'), else display an error message
        if store(request.form['content']):
            return redirect('/')
        else:
            return "There was an issue adding task"
    
# Delete task route
@app.route('/delete/<int:id>')
def delete(id):
    if delete_task(id):
        return redirect('/')
    else : 
        return "There was a problem deleting the task"

# Upate task route
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def upate(id):
    if request.method == "GET":
        task = Todo.query.get_or_404(id)
        
        return display_task(id, 'update.html')
    else:
        new_content = request.form['content']

        if update_task(id, new_content):
            return redirect('/')
        else :
            return "There was an error updating your task."

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)



##### Before factoring into MVC architecture #####
#
# @app.route('/', methods=['POST', 'GET']) # this route can receive post and get
# def index():
#     if request.method == "POST":
#         task_content = request.form['content'] #name='content' in html
#         new_task = Todo(content=task_content)

#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue adding your task'
#     else:
#         tasks = Todo.query.order_by(Todo.date_created).all()
#         print(tasks)
#         return render_template('index.html', tasks=tasks)

# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Todo.query.get_or_404(id)

#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return "There was a problem deleting the task"


# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def upate(id):
#     task = Todo.query.get_or_404(id)

#     if request.method == "POST":
#         task.content = request.form['content']

#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return "There was an error updating"
#     else:
#         return render_template('update.html', task=task)
