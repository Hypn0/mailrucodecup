import os
import json
import zipfile
import tornado.web
import tornado.ioloop
from Models.Users import User
from Models.Visits import Visit
from Models.Locations import Location

from Controllers.Users import Users_controller, Users_create_controller, Users_visits
from Controllers.Visits import Visits_controller, Visits_create_controller
from Controllers.Locations import Locations_controller, Locations_create_controller




os.system("mkdir /tmp/data/")
os.system("cp data.zip /tmp/data/")



def json_extract(filename, json):
    for key, val in json.items():
        if key == 'users':
            for data_dict in val:
                User.create(**data_dict)
        if key == 'locations':
            for data_dict in val:
                Location.create(**data_dict)
        if key == 'visits':
            for data_dict in val:
                Visit.create(**data_dict)


with zipfile.ZipFile("/tmp/data/data.zip", "r") as zfile:
    print(zfile.namelist())
    for filename in zfile.namelist():
        with zfile.open(filename) as f:
            data = json.loads(f.read().decode("utf-8"))
            json_extract(filename, data)
print("unzip done")


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/users/(\d+)", Users_controller),
        (r"/visits/(\d+)", Visits_controller),
        (r"/locations/(\d+)", Locations_controller),

        (r"/users/(\d+)/visits", Users_visits),

        (r"/users/new", Users_create_controller),
        (r"/visits/new", Visits_create_controller),
        (r"/locations/new", Locations_create_controller)
    ])
    app.listen(8080)
    print("run")
    tornado.ioloop.IOLoop.current().start()
