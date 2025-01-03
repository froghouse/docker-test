from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )"""
        )
        conn.commit()
init_db()

@app.route('/')
def index():
    with sqlite3.connect('database.db') as conn:
        posts = conn.execute('SELECT * FROM posts').fetchall()
    return render_template('index.html', posts=posts)


@app.route('/post/<int:id>')
def view_post(id):
    with sqlite3.connect('database.db') as conn:
        post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    if not post:
        return '<h1>Post not found</h1>', 404
    return render_template('post.html', post=post)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        with sqlite3.connect('database.db') as conn:
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)