# IMPORTS
from flask import request                        
from flask.views import MethodView               
from flask_smorest import Blueprint, abort  
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError      

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema                            

# Blueprint in flask_smorest is used to divide APIs into multiple segments
# name "items" is the name where we want to refer later on to create links between 2 blueprints 
blp = Blueprint("items", __name__, description = "Operations on items")



@blp.route("/item/<int:item_id>")          # Connect flask_smorest to the Store Class and the endpoint /item/item_id
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)            # 200 : main successful response
    def get(self, item_id):
        # Run this method when we want to make a request GET in our API
        item = ItemModel.query.get_or_404(item_id)      # Retrieve item from db with primary key or automatically abort if not retrieving
        return item

    @jwt_required()
    def delete(self, item_id):
        # Can delete item only if the user is the admin
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message = "Admin privilege required")

        # Not necessary to decorate these methods since it only returns a message
        # Run this method when we want to make a request DEL in our API
        item = ItemModel.query.get_or_404(item_id)      # Retrieve item from db with primary key or automatically abort if not retrieving
        
        db.session.delete(item)
        db.session.commit()

        return {"message" : "Item is well deleted"}



    
    @blp.arguments(ItemUpdateSchema)                    # The JSON provided by the client is pass though the ItemUpdateSchema, it checks that the fields are there and valid,
                                                        # and then it gives to the method item_data as argument which is the validated dictionary
    @blp.response(200, ItemSchema)                      # The response decorator must be deeper than the arguments decorator

    def put(self,item_data, item_id):                   # The extra parameter item_data goes in front of the route argument
        item = ItemModel.query.get(item_id)             # Retrieve item from db with primary key
        
        if item:                                        # Update item if it exists
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id = item_id, **item_data)               # Create item if it does not exist

        db.session.add(item)       
        db.session.commit()

        return item


@blp.route("/item")          
class ItemList(MethodView):
    @jwt_required()
    @blp.response(201, ItemSchema(many= True))          # returns multiple items as a list
    def get(self):
        return ItemModel.query.all()


    
    @jwt_required(fresh = True)                         # Need of a fresh token to create a new item
    @blp.arguments(ItemSchema)                          # The JSON provided by the client is pass though the ItemSchema, it checks that the fields are there and valid,
                                                        # and then it gives to the method item_data as argument which is the validated dictionary
    
    @blp.response(201, ItemSchema)                      # Returns an item
    def post(self, item_data):                          # The item_data param will is the validated field (a dictionary) that the schema requested
        
        item = ItemModel(**item_data)

        try:                        
            db.session.add(item)    # Try to add item to the database
            db.session.commit()     # Save to disk
        except SQLAlchemyError:
            abort(500, message = "An error occured when inserting the item")

        return item