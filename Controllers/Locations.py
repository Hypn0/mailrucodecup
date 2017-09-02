import tornado.web
from Models.Locations import Location
from playhouse.shortcuts import model_to_dict, dict_to_model

class Locations_controller(tornado.web.RequestHandler):
    async def get(self, location_id):
        try:
            l = Location.get(Location.id == location_id)
        except Exception:
            raise tornado.web.HTTPError(404)
        self.set_header('Content-Type', 'application/json')
        self.write(model_to_dict(l))

    async def post(self, location_id):
        body = tornado.escape.json_decode(self.request.body)
        try:
            u = Location.get(Location.id == location_id)
        except Exception:
            raise tornado.web.HTTPError(404)
        if any(x is None for x in body.values()):
            raise tornado.web.HTTPError(400)
        query = Location.update(**body).where(Location.id == location_id)
        query.execute()
        self.write({})

class Locations_create_controller(tornado.web.RequestHandler):
    async def post(self):
        body = tornado.escape.json_decode(self.request.body)
        if any(x is None for x in body.values()):
            raise tornado.web.HTTPError(400)
        Location.create(**body)
        self.write({})