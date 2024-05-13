import os
import secrets  # used for generating secret key for JWT

from flask import Flask, jsonify 
from flask_smorest import Api 
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
from blocklist import BLOCKLIST
import models                       # Import the folder

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint


# Important to test if the API runs well. In order to test, we have to make requests and receive responses that have to match what is expected
# Two main ways to do that:
# 1. Automated test (not in the course)
# 2. Manual exploratory testing --> use insomnia CLIENT https://insomnia.rest/download to make API requests and receive responses
#                               --> Can also use Postman
# --> Create new Insomnia project --> Create new request collection --> Create requests
# The insomnia client allows to test the app and check if the APIs are working


def create_app(db_url = None):
    # Creation of a Flask app
    app = Flask(__name__)               # Does a lot of things, including being able to run the app ' flask.run ' run the app
    print(__name__)


    ##################################################################################################################################
    # APP CONFIGURATION SETTINGS
    ##################################################################################################################################

    # Doc: https://flask.palletsprojects.com/en/2.3.x/config/

    app.config["PROPAGATE_EXCEPTIONS"] = True       # Exceptions are re-raised rather than being handled by the app’s error handlers. 
                                                    # If not set, this is implicitly true if TESTING or DEBUG is enabled.
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPEN_API_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"                                       # Tell flask_smorest to use swagger for the API doc
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"      # Load swagger code from this url to display documentation
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")         # Connection to a string database. sqlite easy to use 
                                                                                                            # Environment variables are often used when deploying the flask app (easy way to store arbitrary secret or information in our server
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    
    db.init_app(app)                            # Initialize the flask sql alchemy extension giving it the app (can connect flask app to the sql alchemy)

    migrate = Migrate(app, db)                  # Initialize the migrate (must be created after db.init(app))

    api = Api(app)                              # Connect the flask_smorest extension to the Flask app

    app.config["JWT_SECRET_KEY"] = "147265597306848910233636288128545570943"    # secrets.SystemRandom().getrandbits(128) --> Setup of secret key used for signing the JWT (to check if users did not create their own JWT somewhere else)
    jwt = JWTManager(app)                                                       # Create instance of JWT


    @jwt.token_in_blocklist_loader                                              # Function running whenever we receive a jwt
    def check_if_token_in_blocklits(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    

    @jwt.revoked_token_loader                                                   # What receives the user when jwt is revoked
    def revoked_token_callback(wt_header, jwt_payload):
        return (
            jsonify({
                "description" : "The token has been revoked", "error": "token_revoked"
            }), 401
        )


    @jwt.needs_fresh_token_loader                                               # When needing a fresh token and receiving a non-fresh one
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description" : "The token is not fresh",
                    "error" : "fresh_token_required"
                }
            ), 401
        )



    @jwt.additional_claims_loader                                               # Function that runs every time we create a JWT. 
    def add_claims_to_jwt(identity):                                            # identity = identity receives in user.py when creating an access token 
        # Must look in a database and see wheter the user is an admin (better than the condition below)
        if identity == 1:
            return{"is_admin": True}
        return{"is_admin": False}
    


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"message": "The token has expired.", "error": "token_expired"}
            ),
            401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {"description": "Request does not contain an access token", "error": "authorization_required"}
            ),
            401
        )

    with app.app_context():
        db.create_all()
        
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app

