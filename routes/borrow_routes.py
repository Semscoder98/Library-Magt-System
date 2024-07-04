from flask import Blueprint, request, jsonify
from models import db, Book
from auth_routes import auth

bp = Blueprint('borrow', __name__, url_prefix='/borrow')

@bp.route('/<int:book_id>', methods=['POST'])
@auth.login_required
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.quantity < 1:
        return jsonify({'message': 'Book not available'}), 400
    
    book.quantity -= 1
    db.session.commit()
    
    return jsonify({'message': 'Book borrowed successfully'}), 200

@bp.route('/<int:book_id>', methods=['POST'])
@auth.login_required
def return_book(book_id):
    book = Book.query.get_or_404(book_id)
    book.quantity += 1
    db.session.commit()
    
    return jsonify({'message': 'Book returned successfully'}), 200
