from flask import Blueprint, request, jsonify
from models import db, Book
from auth_routes import auth

bp = Blueprint('books', __name__, url_prefix='/books')

@bp.route('/', methods=['POST'])
@auth.login_required
def add_book():
    if auth.current_user().role != 'librarian':
        return jsonify({'message': 'Permission denied'}), 403

    data = request.get_json()
    book = Book(
        title=data['title'],
        author=data['author'],
        genre=data['genre'],
        quantity=data['quantity']
    )
    db.session.add(book)
    db.session.commit()
    
    return jsonify({'message': 'Book added successfully'}), 201

@bp.route('/<int:book_id>', methods=['PUT'])
@auth.login_required
def update_book(book_id):
    if auth.current_user().role != 'librarian':
        return jsonify({'message': 'Permission denied'}), 403
    
    data = request.get_json()
    book = Book.query.get_or_404(book_id)
    book.title = data['title']
    book.author = data['author']
    book.genre = data['genre']
    book.quantity = data['quantity']
    db.session.commit()
    
    return jsonify({'message': 'Book updated successfully'}), 200

@bp.route('/<int:book_id>', methods=['DELETE'])
@auth.login_required
def delete_book(book_id):
    if auth.current_user().role != 'librarian':
        return jsonify({'message': 'Permission denied'}), 403
    
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    
    return jsonify({'message': 'Book deleted successfully'}), 200


@bp.route('/', methods=['GET'])
def search_books():
    title = request.args.get('title')
    author = request.args.get('author')
    genre = request.args.get('genre')
    available = request.args.get('available')
    
    query = Book.query
    if title:
        query = query.filter(Book.title.contains(title))
    if author:
        query = query.filter(Book.author.contains(author))
    if genre:
        query = query.filter(Book.genre.contains(genre))
    if available:
        query = query.filter(Book.quantity > 0)
    
    books = query.all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'quantity': book.quantity} for book in books]), 200
