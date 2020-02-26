from blueprints import db
from flask_restful import fields

class Building(db.Model):
    __tablename__ = "Building"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(1000), nullable = False)
    facilities = db.Column(db.String(1000), nullable = False)
    building_type = db.Column(db.String(50), nullable = False)
    image = db.Column(db.String(1000), nullable = False)
    street = db.Column(db.String(1000), nullable = False)
    city = db.Column(db.String(255), nullable = False)
    country = db.Column(db.String(255), nullable = False)
    longitude = db.Column(db.String(255), nullable = False)
    latitude = db.Column(db.String(255), nullable = False)
    deleted = db.Column(db.Boolean, nullable = False, default=False)

    response_fields = {
        'id' : fields.Integer,
        'name' : fields.String,
        'description' : fields.String,
        'facilities' : fields.String,
        'building_type': fields.String,
        'image': fields.String,
        'street': fields.String,
        'city': fields.String,
        'country': fields.String,
        'longitude': fields.String,
        'latitude': fields.String,
        'deleted': fields.Boolean
    }

    def __init__(self, name, description, facilities, building_type, image, street, city, country, longitude, latitude):
        self.name = name
        self.description = description,
        self.facilities = facilities,
        self.building_type = building_type
        self.image = image
        self.street = street
        self.city = city
        self.country = country
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self):
        return '<Building %r>' %self.id


class Images(db.Model):
    __tablename__ = "Images"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    building_id = db.Column(db.Integer, db.ForeignKey("Building.id"), nullable = False)
    image = db.Column(db.String(1000), nullable = False)
    deleted = db.Column(db.Boolean, nullable = False, default=False)

    response_fields = {
        'id' : fields.Integer,
        'building_id' : fields.Integer,
        'image': fields.String,
        'deleted': fields.Boolean
    }

    def __init__(self, building_id, image):
        self.building_id = building_id
        self.image = image

    def __repr__(self):
        return '<Images %r>' %self.id

