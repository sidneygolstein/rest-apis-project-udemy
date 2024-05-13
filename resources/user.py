from flask import request                        
from flask.views import MethodView               
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256              # Hashing algorithm. Used to hash password sent by client
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity,jwt_required, get_jwt  # Token generated in the server to send it to the client. Can treat the access toke as a proxy to check if the client has logged in 

from db import db
from blocklist import BLOCKLIST 
from models import UserModel    
from schemas import UserSchema

blp = Blueprint("User", "users", description = "Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)  # Takes as arguments the user schema (username & password are required)
    def post(self, user_data):
        # Check if username is unique
        if UserModel.query.filter(UserModel.username  == user_data["username"]).first():
            abort(409, message = "A user with that username already exists")

        user = UserModel(
            username = user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"])     # Encryption of client password
        )
        db.session.add(user)
        db.session.commit()
        return {"message" : "User created successfully"}, 201


# Logout endpoint
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        # Check if user exists
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]).first()
        # If user exists, we check the password
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
             # Creation of access token
             access_token = create_access_token(identity=user.id, fresh= True)
             # Creation of refresh token
             refresh_token = create_refresh_token(identity=user.id)
             return {"access_token" : access_token, "refresh_token": refresh_token}
        abort(401, message = "Invalid credentials")


# Refresh endpoint
@blp.route('/refresh')
class TokenRefresh(MethodView):
    @jwt_required(refresh = True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh = False)   # Create new access token, which is a non-fresh one 
        return {"access_token" : new_token}

# Logout endpoint
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]              # jwt unique identifier or get_jwt().get(jti)
        BLOCKLIST.add(jti)
        return{"message": "Successfully logged out"}


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200,UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message" : "User deleted successfully"}, 201