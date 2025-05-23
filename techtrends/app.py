import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    handlers=[logging.StreamHandler()])

db_connection_count = 0

def get_db_connection():
    global db_connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    db_connection_count += 1
    logging.debug("Database connection established.")
    return connection

def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                              (post_id,)).fetchone()
    connection.close()
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    logging.info("The homepage has been retrieved.")
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        logging.warning("Post not found!")
        return render_template('404.html'), 404
    logging.info(f'The <<{post["title"]}>> post has been retrieved.')
    return render_template('post.html', post=post)

@app.route('/about')
def about():
    logging.info("The about webpage has been retrieved.")
    return render_template('about.html')

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            logging.warning("Post creation failed: Title is required.")
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                               (title, content))
            connection.commit()
            connection.close()
            logging.info(f'The <<{title}>> post has been created successfully.')
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/healthz')
def healthz():
    try:
        connection = get_db_connection()
        connection.execute('SELECT 1 FROM posts LIMIT 1')
        connection.close()
        return jsonify(result="OK - healthy"), 200
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        return jsonify(result="ERROR - unhealthy"), 500

@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    post_count = connection.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
    connection.close()
    return jsonify(db_connection_count=db_connection_count, post_count=post_count), 200

if __name__ == "__main__":
    logging.info("Starting TechTrends application...")
    app.run(host='0.0.0.0', port='3111')

