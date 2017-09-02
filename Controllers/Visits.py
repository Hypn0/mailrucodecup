import tornado.web
from Models.Visits import Visit
from playhouse.shortcuts import model_to_dict, dict_to_model

class Visits_controller(tornado.web.RequestHandler):
    async def get(self, visit_id):
        try:
            v = Visit.get(Visit.id == visit_id)
        except Exception:
            raise tornado.web.HTTPError(404)
        v = model_to_dict(v)
        v['user'] = v['user']['id']
        v['location'] = v['location']['id']
        self.write(v)

    async def post(self, visit_id):
        body = tornado.escape.json_decode(self.request.body)
        try:
            u = Visit.get(Visit.id == visit_id)
        except Exception:
            raise tornado.web.HTTPError(404)
        if any(x is None for x in body.values()):
            raise tornado.web.HTTPError(400)
        query = Visit.update(**body).where(Visit.id == location_id)
        query.execute()
        self.write({})

class Visits_create_controller(tornado.web.RequestHandler):
    async def post(self):
        body = tornado.escape.json_decode(self.request.body)
        if any(x is None for x in body.values()):
            raise tornado.web.HTTPError(400)
        Visit.create(**body)
        self.write({})