from flask_restful import Resource, reqparse
from models import User,db
from utils import generate_access_token

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True)
parser.add_argument('password', type=str, required=True)
parser.add_argument('email', type=str, required=True)

class UserRegistration(Resource):
    def post(self):
        args = parser.parse_args()
        new_user = User(username=args['username'], password=args['password'], email=args['email'], role='user')
        db.session.add(new_user)
        db.session.commit()
        return {"message": "Account successfully created"}, 200

class UserLogin(Resource):
    def post(self):
        args = parser.parse_args()
        user = User.query.filter_by(username=args['username'], password=args['password']).first()
        if user:
            access_token = generate_access_token(user.id)
            return {"status": "Login successful", "status_code": 200, "user_id": user.id, "access_token": access_token}, 200
        else:
            return {"status": "Incorrect username/password provided. Please retry", "status_code": 401}, 401
