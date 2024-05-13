# CREATION OF THE ITEM DB

from db import db               # Get the SQLAlchly instance into item.py

# Has a couple of features that can be used. For example we will be able to say to SQLAlchemy 
# what tables we gonna use in our app and what columns these tables have.
# In addition, any class that we will create that maps to a table with columns, SQLAlchemy wil
# be automatically able to handle turning those tables rows into python objects


# CREATION OF THE ITEM DB

class ItemModel(db.Model):
    __tablename__ = "items"                                                             # Creation of a table called "items"

    id = db.Column(db.Integer, primary_key=True)                                        # Definition of a column that will be part of the "items" table. 
                                                                                        # The id is by default auto-incrementing
    name = db.Column(db.String(80), unique = True, nullable = False)                    # nullable = False --> items must have names, unique = True --> items must
                                                                                        # have different names
    description = db.Column(db.String)
    price = db.Column(db.Float(precision = 5), unique = False, nullable = False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id") ,unique = False, nullable = False)     # Will be a link between the item table and the store table. 
                                                                                                        # This value will have to match the id value in the store table  
                                                                                                        # db.ForeignKey(table.column) allows to map that a item has
                                                                                                        # a store_id and belongs to a store
    store = db.relationship("StoreModel", back_populates = "items")                                     # Populate a store variable with a StoreModel object whose id matches the foreignKey 
    tags = db.relationship("TagModel", back_populates = "items", secondary = "items_tags")              # 'items' should match the 'items' in tag.py
