from flask_restful import Resource, reqparse
from models.Users import Users
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
import os 


class UserRegister(Resource):
    # Ensuring that a user has a password and a name
    parser = reqparse.RequestParser()

    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    parser.add_argument(
        "admin_password", 
        type=str,
        required=True,
        help="Please provide the admin_password argument in order to register new users."
    )

    def post(self):
        data = UserRegister.parser.parse_args()
 
        # Checking if the post request is made with admin rights 
        if data.get('admin_password') != os.environ.get("ADMIN_PASSWORD"):
            return {"message": "Incorrect admin password"}, 400

        if Users.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        # Creating the hash
        hashed = md5(f"{data['password']}{os.environ['SECRET_KEY']}".encode())

        user = Users(data['username'], hashed.hexdigest())
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    
    parser.add_argument(
        "admin_password", 
        type=str,
        required=True,
        help="Please provide the admin_password argument in order to manipulate users."
    )

    def get(self):
        data = User.parser.parse_args()

        # Checking if the post request is made with admin rights 
        if data.get('admin_password') != os.environ.get("ADMIN_PASSWORD"):
            return {"message": "Incorrect admin password"}, 400

        usr = Users.query.filter_by(username=data['username']).first()

        if usr: 
            return usr.json()
        else:
            return {"message": f"User {data['username']} does not exist"}, 400

    def delete(self):
        data = User.parser.parse_args()

        # Checking if the post request is made with admin rights 
        if data.get('admin_password') != os.environ.get("ADMIN_PASSWORD"):
            return {"message": "Incorrect admin password"}, 400

        usr = Users.query.filter_by(username=data['username']).first()

        if usr: 
            usr.delete_from_db()
            return {'message': f"User {data['username']} deleted."}, 200
        else:
            return {"message": f"User {data['username']} does not exist"}, 400
