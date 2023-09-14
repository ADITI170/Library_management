from flask_restful import Resource, reqparse
from models import User, Book, Booking
from utils import generate_access_token, validate_access_token
from datetime import datetime, timedelta
from models import db, User 
from flask import request

# Define a parser to handle request data
parser = reqparse.RequestParser()

# User Registration
class UserRegistration(Resource):
    def post(self):
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()
        
        # Check if the user already exists
        existing_user = User.query.filter_by(username=args['username']).first()
        if existing_user:
            return {"message": "Username already exists"}, 400
        
        new_user = User(username=args['username'], password=args['password'], email=args['email'], role='user')
        db.session.add(new_user)
        db.session.commit()
        return {"message": "Account successfully created"}, 200

# User Login
class UserLogin(Resource):
    def post(self):
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        
        user = User.query.filter_by(username=args['username'], password=args['password']).first()
        if user:
            access_token = generate_access_token(user.id)
            return {"status": "Login successful", "status_code": 200, "user_id": user.id, "access_token": access_token}, 200
        else:
            return {"status": "Incorrect username/password provided. Please retry", "status_code": 401}, 401

# Admin endpoint to add a new book
class AddNewBook(Resource):
    def post(self):
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('author', type=str, required=True)
        parser.add_argument('isbn', type=str, required=True)
        args = parser.parse_args()
        
        new_book = Book(title=args['title'], author=args['author'], isbn=args['isbn'])
        db.session.add(new_book)
        db.session.commit()
        return {"message": "Book added successfully", "book_id": new_book.id}, 200

# User endpoint to get book availability
class GetBookAvailability(Resource):
    def get(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {"message": "Book not found"}, 404
        
        now = datetime.utcnow()
        booking = Booking.query.filter_by(book_id=book_id).filter(Booking.return_time > now).first()
        if booking:
            return {"book_id": book_id, "available": False, "next_available_at": booking.return_time}, 200
        else:
            return {"book_id": book_id, "available": True}, 200

# User endpoint to borrow a book
class BorrowBook(Resource):
    def post(self):
        parser.add_argument('book_id', type=int, required=True)
        parser.add_argument('issue_time', type=str, required=True)
        parser.add_argument('return_time', type=str, required=True)
        args = parser.parse_args()
        
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return {"status": "Authorization token is missing"}, 401
        
        token = auth_header.split(' ')[1]
        user_id = validate_access_token(token)
        if not user_id:
            return {"status": "Invalid or expired authorization token"}, 401
        
        book_id = args['book_id']
        issue_time = datetime.strptime(args['issue_time'], "%Y-%m-%dT%H:%M:%SZ")
        return_time = datetime.strptime(args['return_time'], "%Y-%m-%dT%H:%M:%SZ")
        
        now = datetime.utcnow()
        booking = Booking.query.filter_by(book_id=book_id).filter(Booking.return_time > now).first()
        if booking:
            return {"status": "Book is already booked until", "status_code": 400, "next_available_at": booking.return_time}, 400
        
        new_booking = Booking(user_id=user_id, book_id=book_id, issue_time=issue_time, return_time=return_time)
        db.session.add(new_booking)
        db.session.commit()
        return {"status": "Book booked successfully", "status_code": 200, "booking_id": new_booking.id}, 200

