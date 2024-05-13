# FILE WHERE WE WILL PUT OUR MARSHMALLOW SCHEMAS
# Marshmallow exists to make data validations

from marshmallow import Schema, fields

# Schemas are used for validating incoming data. It will check the data incoming from the clients and check if it respects the schemas

# An item has: 
#   - id
#   - name
#   - price
#   - store_id

class PlainItemSchema(Schema):                  # Item schema that doesn't know anything about stores (doesn't deal with stores)
    # Definition of the fields and how they behave in terms of inputs and outputs
    id = fields.Int(dump_only=True)             # This field is only used to returning dat / when sending data back
    name = fields.Str(required = True)          # It is needed and required for validation when receiving incoming data
    price = fields.Float(required = True)       # Required for validation

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)             
    name = fields.Str(required = True)   

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)             
    name = fields.Str(required = True) 
    

class ItemUpdateSchema(Schema):
    name = fields.Str()                         # Not required, either or both can be missing        
    price = fields.Float()                      # Not required
    store_id = fields.Int()                     # Not required



class ItemSchema(PlainItemSchema):                              # Is composed of a plain item + a store id --> Whenever we use ItemSchema,
                                                                # we will pass the store_id when receiving data from the client 
    store_id = fields.Int(required = True, load_only = True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only = True)


class StoreSchema(PlainStoreSchema):                    # Is composed of a list of items and tags
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


    # When nesting, we can only use part of the fields. This is the reason why we first define a PlainItemSchema as well as a PlainStoreSchema


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only = True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)    
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)



class UserSchema(Schema):
    id = fields.Int(dump_only=True)                                 # We never receive an id from the client
    username = fields.Str(required = True)
    password = fields.Str(required = True, load_only = True)        # API never returns user password, only info about the user