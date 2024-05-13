from db import db 

# One item can have multiple tags, and vice versa

class ItemTagsModel(db.Model):
    __tablename__ = "items_tags"

    id = db.Column(db.Integer, primary_key=True)

    # The next 2 columns are a link to items and a link to tags. 
    #  These columns will define the relationships between any individual item and any individual tag

    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
