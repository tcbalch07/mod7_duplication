from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
import pymysql

books_bp = Blueprint('books', __name__)

@books_bp.route('/catalog', methods=['GET', 'POST'])
def catalog():
    db = get_db()
    cursor = db.cursor()

    # Get the selected book ID from the dropdown if any
    book_id_filter = request.args.get('book_id')

    # Query to fetch books with their average rating, price, and description
    if book_id_filter:
        cursor.execute("""
            SELECT b.books_id, b.title, b.author, b.price, b.description, AVG(r.rating) AS avg_rating
            FROM books b
            LEFT JOIN reviews r ON b.books_id = r.book_id
            WHERE b.books_id = %s
            GROUP BY b.books_id
        """, (book_id_filter,))
    else:
        cursor.execute("""
            SELECT b.books_id, b.title, b.author, b.price, b.description, AVG(r.rating) AS avg_rating
            FROM books b
            LEFT JOIN reviews r ON b.books_id = r.book_id
            GROUP BY b.books_id
        """)

    books = cursor.fetchall()  # This should give a list of books with their avg_rating, price, and description

    cursor.close()
    db.close()

    # Pass the books to the template
    return render_template('catalog.html', books=books)

@books_bp.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']
        description = request.form['description']  # Added description field

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO books (title, author, price, description) VALUES (%s, %s, %s, %s)", (title, author, price, description))  # Added description here
        db.commit()
        flash('Book added successfully!')
        return redirect(url_for('books.catalog'))
    return render_template('add_book.html')

@books_bp.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    # Your logic to edit the book details
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM books WHERE books_id = %s", (book_id,))
    book = cursor.fetchone()

    if request.method == 'POST':
        # Your logic to update the book in the database
        cursor.execute("UPDATE books SET title = %s, author = %s, price = %s, description = %s WHERE books_id = %s",
                       (request.form['title'], request.form['author'], request.form['price'], request.form['description'], book_id))  # Updated with description
        get_db().commit()
        return redirect(url_for('books.catalog'))  # Redirect back to catalog page

    return render_template('update_book.html', book=book)

@books_bp.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    db = get_db()
    cursor = db.cursor()

    try:
        # First, delete the reviews related to the book
        cursor.execute("DELETE FROM reviews WHERE book_id = %s", (book_id,))
        db.commit()

        # Then, delete the book itself
        cursor.execute("DELETE FROM books WHERE books_id = %s", (book_id,))
        db.commit()

        flash('Book and associated reviews deleted successfully!', 'success')
    except Exception as e:
        flash(f"Error: {str(e)}", 'danger')
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('books.catalog'))


@books_bp.route('/review/<int:book_id>', methods=['POST'])
def add_review(book_id):
    review = request.form['review']
    rating = request.form['rating']

    db = get_db()
    cursor = db.cursor()

    # Insert the review into the reviews table
    cursor.execute("INSERT INTO reviews (book_id, review_text, rating) VALUES (%s, %s, %s)", (book_id, review, rating))
    db.commit()

    flash('Review added successfully!')
    return redirect(url_for('books.book_details', book_id=book_id))  # Redirect to the book's detail page


@books_bp.route('/book_details/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    connection = get_db()
    cursor = connection.cursor(pymysql.cursors.DictCursor)  # Use DictCursor to return dictionaries

    # Query for the book details
    cursor.execute("SELECT * FROM books WHERE books_id = %s", (book_id,))
    book = cursor.fetchone()

    # Query for the reviews for this book (use review_text instead of review)
    cursor.execute("SELECT * FROM reviews WHERE book_id = %s", (book_id,))
    reviews = cursor.fetchall()

    # Close the connection
    cursor.close()
    connection.close()

    return render_template('book_details.html', book=book, reviews=reviews)

@books_bp.route('/events', methods=['GET', 'POST'])
def events():
    return render_template('events.html')
