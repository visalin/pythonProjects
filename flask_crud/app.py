from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

# Step A: Initialize the Database with a `tasks` table if it doesn’t exist.

def init_db():
    conn = sqlite3.connect('day11_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0
     )

    ''')
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect('day11_database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
    conn.commit()
    conn.close()
    flash('Task added successfully', 'success')
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    flash('Task deleted successfully', 'danger')
    return redirect('/')

@app.route('/deleteall')
def delete_all_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE from tasks')
    conn.commit()
    conn.close()
    flash('Deleted all the tasks successfully', 'danger')
    return redirect('/')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    flash('Task marked as completed', 'success')
    return redirect('/')

@app.route('/edit/<int:task_id>')
def edit_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    conn.close()
    return render_template('edit.html', task=task)

@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    title = request.form['title']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET title = ? WHERE id = ?', (title, task_id))
    conn.commit()
    conn.close()
    flash('Task updated successfully', 'success')
    return redirect('/')

@app.route('/uncompleted')
def show_uncompleted():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE completed = 0')  # Select only uncompleted tasks
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
