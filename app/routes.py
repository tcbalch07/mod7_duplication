from flask import render_template
from . import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/book/<int:book_id>')
def book_details(book_id):
    return f"<h1>Book Details</h1><p>Placeholder for book {book_id} details.</p>"


