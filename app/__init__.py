from flask import Flask, render_template, session
from app.blueprints.books import books_bp
from app.db_connect import close_db

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    # Register Blueprints
    app.register_blueprint(books_bp, url_prefix='/books')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.teardown_appcontext
    def teardown_db(exception=None):
        close_db(exception)

    return app