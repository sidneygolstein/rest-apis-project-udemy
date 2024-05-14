# CREATION OF THE MODEL DB FOR TAG

from db import db 

class TagModel(db.Model):
    __tablename__ =  "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable = False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable = False)

    store = db.relationship("StoreModel", back_populates = "tags")   # 'tags' here should be the same as 'tags' in store.py
    items = db.relationship("ItemModel", back_populates = "tags", secondary = "items_tags") # Has to go through the secondary table in order to find what items these tag is related to
