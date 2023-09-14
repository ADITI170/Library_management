from flask import Flask
from flask_restful import Api
from models import db
from resources import UserRegistration, UserLogin, GetBookAvailability, BorrowBook

app = Flask(__name__)
app.config.from_object('config')  # Load configuration from config.py
db.init_app(app)
api = Api(app)

# Define your routes and add resources here
api.add_resource(UserRegistration, '/api/signup')
api.add_resource(UserLogin, '/api/login')
#api.add_resource(AddNewBook, '/api/books/create')
#api.add_resource(SearchBooksByTitle, '/api/books')
api.add_resource(GetBookAvailability, '/api/books/<int:book_id>/availability')
api.add_resource(BorrowBook, '/api/books/borrow')

if __name__ == '__main__':
    app.run(debug=True)
