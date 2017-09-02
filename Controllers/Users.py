import tornado.web
from Models.Users import User
from Models.Visits import Visit
from Models.Locations import Location
from playhouse.shortcuts import model_to_dict, dict_to_model

class Users_controller(tornado.web.RequestHandler):
    async def get(self, user_id):
        try:
            u = User.get(User.id == user_id)
        except Exception:
            raise tornado.web.HTTPError(404)
        self.set_header('Content-Type', 'application/json')
        self.write(model_to_dict(u))

    async def post(self, user_id):
        body = tornado.escape.json_decode(self.request.body)
        try:
            u = User.get(User.id == user_id)
        except Exception:
            raise tornado.web.HTTPError(404)
        if any(x is None for x in body.values()):
            raise tornado.web.HTTPError(400)
        query = User.update(**body).where(User.id == location_id)
        query.execute()
        self.write({})

class Users_create_controller(tornado.web.RequestHandler):
     async def post(self):
        body = tornado.escape.json_decode(self.request.body)
        if any(x is None for x in body.values()):
            raise tornado.web.HTTPError(400)
        User.create(**body)
        self.write({})

class Users_visits(tornado.web.RequestHandler):
    async def get(self, user_id):
        visits = Visit.select().join(User).switch(Visit).join(Location).where(User.id == user_id)

        if 'fromDate' in self.request.arguments:
            visits = visits.where(Visit.visited_at > self.request.arguments['fromDate'])
        if 'toDate' in self.request.arguments:
            visits = visits.where(Visit.visited_at < self.request.arguments['toDate'])
        if 'country' in self.request.arguments:
            visits = visits.where(Location.country == self.request.arguments['country'])
        if 'toDistance' in self.request.arguments:
            visits = visits.where(Location.distance < self.request.arguments['toDistance'])
        visits = visits.order_by(Visit.visited_at).dicts()
        self.write({'visits':[c for c in visits]})


