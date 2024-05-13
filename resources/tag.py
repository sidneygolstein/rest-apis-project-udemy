# Creation of the API endpoints for tag
# One item can have multiple tags. One tag can be assigned to multiple items --> many to many 

from flask import request                        
from flask.views import MethodView               
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError      

from db import db
from models import TagModel, StoreModel, ItemModel       
from schemas import TagSchema, TagAndItemSchema    


blp = Blueprint("Tags", "tags", description = "Operations on tags")

@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):

    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):                        # Get a list of tags registered under a given store
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):

        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first(): # Check if tag with that name already exists in that store
            abort(400, message = "Tag with that name already exists in that store")

        tag = TagModel(**tag_data, store_id = store_id)     # Create a tag

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message = str(e)
            )

        return tag

# Class for linking/unlinking tags to items
@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    # Does not create any tag or item (these were already created) 
    @blp.response(200, TagSchema)
    def post(self, item_id, tag_id):
        # Find item and tag and make sur it exists
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)   # Append to the tags list of the item the new tag
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message = str(e))

        return tag
    


    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        # Find item and tag and make sur it exists
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)   # Remove to the tags list of the item the new tag
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message = str(e))

        return {"message" : "Item removed from tag", "item": item, "tag": tag}

        
         



# Retrieve info for a specific tag
@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    

    @blp.response(
        202,
        description = "Deletes a tag if no item is tagged with it",
        example = {"message": "Tag deleted."}
    )
    @blp.alt_response(404, description = "Tag not found") # When aiming to document alternative responses (not just only the main)
    @blp.alt_response(400, description = "Returned if the tag is assigned to one or more items. In this case, the tag is not deleted") 

    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)      # Delete tag if not assigned to any item
            db.session.commit()
            return {"message" : "Tag deleted"}
        abort(400,
              message = "Could not delete tag. Make sure tag is not assigned to any items, then try again.")
        