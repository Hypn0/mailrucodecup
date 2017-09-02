import os
import json
import zipfile
import sqlite3
import asyncio
# from sqlalchemy import create_engine
from aiohttp import web


def json_extract(filename, json):
    for key, val in json.items():
        for item in val:
            push_to_db(key, item)

def push_to_db(key, item):
    if key == 'users':
        i = (item['id'], item['email'], item["first_name"], item['last_name'], item["gender"], item["birth_date"])
        c.execute("INSERT INTO users (id, email,first_name, last_name, gender, birth_date) VALUES (?,?,?,?,?,?);", i)
    if key == 'locations':
        i = (item['id'], item['place'], item["country"], item['city'], item["distance"])
        c.execute("INSERT INTO locations (id, place, country, city, distance) VALUES (?,?,?,?,?);", i)
    if key == 'visits':
        i = (item['id'], item['location'], item["user"], item['visited_at'], item["mark"])
        c.execute("INSERT INTO visits (id, location, user, visited_at, mark) VALUES (?,?,?,?,?);", i)


os.system("mkdir /tmp/data/")
os.system("cp data.zip /tmp/data/")


# engine = create_engine('sqlite:///:memory:', echo=True)

db = sqlite3.connect(":memory:")
c = db.cursor()
c.execute("CREATE TABLE users       (id INTEGER, email VARCHAR(100),first_name VARCHAR(50), last_name INTEGER(50), gender VARCHAR(1), birth_date DATETIME);")
c.execute("CREATE TABLE locations   (id INTEGER, place TEXT, country VARCHAR(50), city VARCHAR(50), distance INTEGER);")
c.execute("CREATE TABLE visits      (id INTEGER, location INTEGER, user INTEGER, visited_at TIMESTAMP, mark INTEGER);")

print(os.system("ls -al /tmp/data"))

with zipfile.ZipFile("/tmp/data/data.zip", "r") as zfile:
    for filename in zfile.namelist():
        print(filename)
        with zfile.open(filename) as f:
            print(filename)
            data = json.loads(f.read().decode("utf-8"))
            json_extract(filename, data)
print("unzip done")

print('here 4')
def users(request):
    print('here 3')
    id = request.match_info['id']
    try:
        int(id)
    except ValueError:
        return web.json_response({"error": "bad param"}, status=404)
    c.execute("SELECT * FROM users where `id`= %s  ;" % id)
    try:
        res = c.fetchall()[0]
    except IndexError:
        return web.json_response({"error": "not found"}, status=404)
    else:
        r = {
            "id":res[0],
            "email": res[1],
            "first_name": res[2],
            "last_name": res[3],
            "gender": res[4],
            "birth_date": res[5]
        }
    return web.json_response(r)


print('here 1')




app = web.Application()
app.router.add_get('/users/{id}', users)
print('here 2')


port = 8080
if os.path.exists('options.txt'):
    port = 80
print("run on port %s" % port)
web.run_app(app, host='127.0.0.1', port=port)
print('here 5')