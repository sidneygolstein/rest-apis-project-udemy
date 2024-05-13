# IMPORTS

import uuid                                     
from flask import request                        
from flask.views import MethodView               
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError      

from db import db
from models import StoreModel       
from schemas import StoreSchema               

# Blueprint in flask_smorest is used to divide APIs into multiple segments
# name "stores" is the name where we want to refer later on to create links between 2 blueprints 
blp = Blueprint("stores", __name__, description = "Operations on stores")

# Class methodView allows to create a classes whose methods route to specific endpoints

@blp.route("/store/<int:store_id>")          # Connect flask_smorest to the Store Class and the endpoint /store/store_id
class Store(MethodView):
    
    @blp.response(200, StoreSchema)             # Returns a store
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)      # Retrieve store from db with primary key or automatically abort if not retrieving
        return store

    def delete(self, store_id):
        # Not necessary to decorate these methods since it only returns a message
        # Run this method when we want to make a request DEL in our API
        store = StoreModel.query.get_or_404(store_id)      # Retrieve store from db with primary key or automatically abort if not retrieving

        db.session.delete(store)
        db.session.commit()

        return {"message" : "Store is well deleted"}  


@blp.route("/store")          # Connect flask_smorest to the Store Class and the endpoint /store
class StoreList(MethodView):

    @blp.response(201, StoreSchema(many=True))          # Returns many stores as a list
    def get(self):
        # Run this method when we want to make a request GET in our API
        return StoreModel.query.all()


    @blp.arguments(StoreSchema)                         # The JSON provided by the client is pass though the StoreSchema, it checks that the fields are there and valid,
                                                        # and then it gives to the method item_data as argument which is the validated dictionary
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:                        
            db.session.add(store)    # Try to add item to the database
            db.session.commit()     # Save to disk
        except IntegrityError:
            abort(400, message = "A store with that name already exists")
        except SQLAlchemyError:
            abort(500, message = "An error occured creating the store")

        return store
    

