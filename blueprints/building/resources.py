from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from blueprints import db, app
from blueprints.building.model import Building, Images

bp_building = Blueprint('building',__name__)
api = Api(bp_building)

class BuildingResources(Resource):

    def get(self): 
        parser = reqparse.RequestParser()
        parser.add_argument('type', location='args', help='invalid type value', choices=('apartment','office'))
        args = parser.parse_args()

        if args['type'] is not None:
            qry_building = Building.query.filter_by(building_type=args['type']).filter_by(deleted=False)
        else :
            qry_building = Building.query.filter_by(deleted = False)

        buildings = []
        for building in qry_building:
            marshal_building = marshal(building, Building.response_fields)
            buildings.append(marshal_building)

        return buildings, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location = 'json', required = True)
        parser.add_argument('description', location = 'json', required = True)
        parser.add_argument('facilities', location = 'json', required = True)
        parser.add_argument('building_type', location = 'json', required = True)
        parser.add_argument('image', location = 'json', required = True)
        parser.add_argument('street', location = 'json', required = True)
        parser.add_argument('city', location = 'json', required = True)
        parser.add_argument('country', location = 'json', required = True)
        parser.add_argument('longitude', location = 'json', required = True)
        parser.add_argument('latitude', location = 'json', required = True)
        args = parser.parse_args()

        building = Building(args['name'], args['description'], args['facilities'], args['building_type'], args['image'], args['street'], args['city'], args['country'], args['longitude'], args['latitude'])
        db.session.add(building)
        db.session.commit()

        app.logger.debug('DEBUG : %s', building)

        return marshal(building, Building.response_fields), 200

    def options(self):
        return {}, 200

class BuildingResourcesId(Resource):
    def get(self, id): 

        qry_building = Building.query.get(id)
        qry_image = Images.query.filter_by(building_id = qry_building.id).filter_by(deleted=False)

        marshal_building = marshal(qry_building, Building.response_fields)

        other_images = []
        for image in qry_image:
            marshal_image = marshal(image, Images.response_fields)
            other_images.append(marshal_image['image'])

        marshal_building['other_images'] = other_images

        return marshal_building, 200

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location = 'json')
        parser.add_argument('description', location = 'json')
        parser.add_argument('facilities', location = 'json')
        parser.add_argument('building_type', location = 'json')
        parser.add_argument('image', location = 'json')
        parser.add_argument('street', location = 'json')
        parser.add_argument('city', location = 'json')
        parser.add_argument('country', location = 'json')
        parser.add_argument('longitude', location = 'json')
        parser.add_argument('latitude', location = 'json')
        parser.add_argument('deleted', location = 'json')
        args = parser.parse_args()

        qry_building = Building.query.get(id)

        if args['name'] is not None:
            qry_building.name = args['name']
        if args['description'] is not None:
            qry_building.description = args['description']
        if args['facilities'] is not None:
            qry_building.facilities = args['facilities']
        if args['building_type'] is not None:
            qry_building.building_type = args['building_type']
        if args['image'] is not None:
            qry_building.image = args['image']
        if args['street'] is not None:
            qry_building.street = args['street']
        if args['city'] is not None:
            qry_building.city = args['city']
        if args['country'] is not None:
            qry_building.country = args['country']
        if args['longitude'] is not None:
            qry_building.longitude = args['longitude']
        if args['latitude'] is not None:
            qry_building.latitude = args['latitude']
        if args['deleted'] is not None:
            qry_building.deleted = True

        db.session.commit()

        return {'message':'edit building success'}, 200
    
    def options(self):
        return {}, 200
class BuildingImageResources(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('building_id', location = 'json', required = True)
        parser.add_argument('image', location = 'json', required = True)
        args = parser.parse_args()

        image = Images(args['building_id'], args['image'])
        db.session.add(image)
        db.session.commit()

        app.logger.debug('DEBUG : %s', image)

        return marshal(image, Images.response_fields), 200

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('building_id', location = 'json')
        parser.add_argument('image', location = 'json')
        parser.add_argument('deleted', location = 'json')
        args = parser.parse_args()

        qry_image = Images.query.get(id)

        if args['building_id'] is not None:
            qry_image.building_id = args['building_id']
        if args['image'] is not None:
            qry_image.image = args['image']
        if args['deleted'] is not None:
            qry_image.deleted = True

        db.session.commit()

        return {'message':'edit image success'}, 200

    def options(self):
        return {}, 200

api.add_resource(BuildingResources,'')
api.add_resource(BuildingResourcesId, '/<int:id>')
api.add_resource(BuildingImageResources,'/image', '/image/<int:id>')