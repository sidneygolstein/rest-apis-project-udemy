# CREATION OF THE STORE DB

from db import db               # Get the SQLAlchly instance into item.py

# Has a couple of features that can be used. For example we will be able to say to SQLAlchemy 
# what tables we gonna use in our app and what columns these tables have.
# In addition, any class that we will create that maps to a table with columns, SQLAlchemy wil
# be automatically able to handle turning those tables rows into python objects

class StoreModel(db.Model):
    __tablename__ = "stores"                                                            # Creation of a table called "stores"

    id = db.Column(db.Integer, primary_key=True)                                        # Definition of a column that will be part of the "stores" table. The id is by default auto-incrementing
    name = db.Column(db.String(80), unique= True, nullable = False)                    # nullable = False --> stores must have names, unique = True --> stores must have different names
    items = db.relationship("ItemModel", back_populates = "store", lazy = "dynamic", cascade = "all, delete")   
    # Allow each StoreModel object to easily see all the items that are associated to him
    # lazy = "dynamic" --> items are not going to be fetched from the DB until we tell to. 
    # cascade = "all, delete" allows to delete the items within a store when a store is deleted --> since items are children of store

    tags = db.relationship("TagModel", back_populates = "store", lazy = "dynamic")    # The 'store' must match the 'store' in tag.py