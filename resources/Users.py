from flask_restful import Resource, reqparse
from models.Users import Users
from werkzeug.security import generate_password_hash, check_password_hash


class UserRegister(Resource):
    # Ensuring that a user has a password and a name
    parser = reqparse.RequestParser()

    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if Users.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = Users(data['username'], generate_password_hash(data['password']))
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class AllUsers(Resource):

    def get(self):
        return [x.json() for x in Users.query.all()]