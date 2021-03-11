from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from models.users import AuthModel
from werkzeug.security import safe_str_cmp
from CustomDecorators import *
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity,create_access_token 
blocklist = set()

class Registration(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('username', type=str, required=True, help="Username is required")
    parse.add_argument('password', type=str, required=True, help="Password is required")
    parse.add_argument('role', type=str, default="Customer")
    parse.add_argument('city', type=str, required=True,
                       help="City is required")
    parse.add_argument('phone', type=str, required=True,
                       help="Phone Number is required")

    def post(self):
        data = Registration.parse.parse_args()

        user = AuthModel.find_by_username(data['username'])

        if user:
            return {
                "AlreadyExistError": {
                    "error": "Username already exist"
                }
            }, 400 
        user = AuthModel(**data)
        user.save_to_db()

        return {
            "message": "User Created Successfully",
        }, 201

class UserLogin(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('username', type=str, required=True, help="Username is required")
    parse.add_argument('password', type=str, required=True, help="Password is required")

    def post(self):
        data = UserLogin.parse.parse_args()
        user = AuthModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            return {
                "role": user.role,
                "access_token": access_token,
            }, 200
        return {
            "error": "Username or Password may incorrect"
        }, 400

class UserLogout(Resource):
    @jwt_required()
    def get(self):
        users = AuthModel.find_by_id(get_jwt_identity())
        if users:
            jti = get_jwt()['jti']
            blocklist.add(jti)
            return {
                "message": "User Logged out Successfully",
                "Status" : "Success"}

        return {"Status": "Fail"}, 200

# class User(Resource):
#     @jwt_required
#     def get(self):
#         user = AuthModel.find_by_id(get_jwt_identity())
#         return {
#             "User": user.json(),
#             "status": 'ok'
#         }

class User(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('username', type=str, required=True,
                       help="Username is required")
    def get(self):
        users = [user.json() for user in AuthModel.query.all()]
        return {"TotalUsers": len(users), "Users": users,  "status": 'ok'}, 200
   
    @jwt_required()
    def delete(self):
        data = User.parse.parse_args()
        user = AuthModel.find_by_username(data['username'])
        print("USER = ", user)
        if user:
            user.delete_from_db()
            return {
                "message": "User DELETED Successfully"
            }, 200

        return {
            "message": "No data"
        }, 400

    @jwt_required()
    def put(self, id):
        parse = reqparse.RequestParser()
        parse.add_argument('username', type=str)
        parse.add_argument('password', type=str)
        parse.add_argument('role', type=str)
        parse.add_argument('city', type=str)
        parse.add_argument('phone', type=str)

        user = AuthModel.find_by_id(id)
        
        if user:
            data = parse.parse_args()
            user.username = data['username']
            user.password = data['password']
            user.city = data['city']
            user.phone= data['phone'] 
            user.save_to_db()
            return {"updated": True, "data": user.json()}, 200
