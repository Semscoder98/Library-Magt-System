from flask import Flask
from flask_migrate import Migrate
from models import db, User, Book

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
migrate = Migrate(app, db)

from routes import auth_routes, book_routes, borrow_routes

app.register_blueprint(auth_routes.bp)
app.register_blueprint(book_routes.bp)
app.register_blueprint(borrow_routes.bp)

if __name__ == '__main__':
    app.run(debug=True)
