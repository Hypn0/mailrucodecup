# examples/1_hello/hello.py
import os
import json
import zipfile
import sqlite3
import asyncio
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

db = sqlite3.connect(":memory:")
c = db.cursor()
c.execute("CREATE TABLE users       (id INTEGER, email VARCHAR(100),first_name VARCHAR(50), last_name VARCHA INTEGERR(50), gender VARCHAR(1), birth_date DATETIME);")
c.execute("CREATE TABLE locations   (id INTEGER, place TEXT, country VARCHAR(50), city VARCHAR(50), distance INTEGER);")
c.execute("CREATE TABLE visits      (id INTEGER, location INTEGER, user INTEGER, visited_at TIMESTAMP, mark INTEGER);")


with zipfile.ZipFile("/tmp/data/data.zip", "r") as zfile:
    for filename in zfile.namelist():
        with zfile.open(filename) as f:
            print(filename)
            data = json.loads(f.read().decode("utf-8"))
            json_extract(filename, data)
print("unzip done")
# c.execute("SELECT * FROM users limit 10;")
# print(c.fetchall())

async def locations(request):
    id = request.match_info['id']
    try:
        int(id)
    except ValueError:
        return web.json_response({"error": "bad param"}, status=400)
    c.execute("SELECT * FROM locations where `id`= %s  ;" % id)
    try:
        res = c.fetchall()[0]
    except IndexError:
        return web.json_response({"error": "not found"}, status=404)
    else:
        r = {
            "id":res[0],
            "place": res[1],
            "country": res[2],
            "city": res[3],
            "distance": res[4]
        }
        return web.json_response(r)

async def users(request):
    id = request.match_info['id']
    try:
        int(id)
    except ValueError:
        return web.json_response({"error": "bad param"}, status=400)
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

async def visits(request):
    id = request.match_info['id']
    try:
        int(id)
    except ValueError:
        return web.json_response({"error": "bad param"}, status=400)
    c.execute("SELECT * FROM visits where `id`= %s  ;" % id)
    try:
        res = c.fetchall()[0]
    except IndexError:
        return web.json_response({"error": "not found"}, status=404)
    else:
        r = {
            "id":res[0],
            "location": res[1],
            "user": res[2],
            "visited_at": res[3],
            "mark": res[4]
        }
        return web.json_response(r)


async def user_visits(request):

    id = request.match_info['id']
    c.execute("SELECT  visits.mark, visits.visited_at, locations.place, locations.country, locations.distance FROM visits join users on visits.user = users.id join locations  on visits.location ==locations.id where users.id = %s ORDER BY visits.visited_at ASC;" % id)
    res = c.fetchall()
    if not res:

         return web.json_response({"error" : "nothing found"}, status=404)
    if 'fromDate' in request.match_info:
        try:
            int(request.match_info['fromDate'])
        except ValueError:
            return request.json_response({"error": "bad param"}, status=400)
        else:
            res = list(filter(lambda x: x[1] > int(request.match_info['fromDate']) , res))

    if 'toDate' in request.match_info:
        try:
            int(request.match_info['toDate'])
        except ValueError:
            return web.json_response({"error": "bad param"}, status=400)
        else:
            res = list(filter(lambda x: x[1] < int(request.match_info['toDate']) , res))

    if 'country' in request.match_info:
        res = list(filter(lambda x: x[3] == request.match_info['country'], res))

    if 'toDistance' in request.match_info:
        try:
            int(request.match_info['toDistance'])
        except ValueError:
            return web.json_response({"error": "bad param"}, status=400)
        else:
            res = list(filter(lambda x: x[4] < int(request.match_info['toDistance']), res))

    q = []

    for r in res:
        q.append({
            "mark":         r[0],
            "visited_at":   r[1],
            "place":        r[2]
        })
    r = {"visits": q}
    return web.json_response(r, status=200)


async def users_update(request):
    print('i am users_update')
    return web.json_response({}, status=200)

async def user_visits_update(request):
    return web.json_response(code=400, json={"error": "bad param"})


async def locations_update(request):
    return web.json_response(code=400, json={"error": "bad param"})


app = web.Application()
app.router.add_get('/users/{id}', users)
app.router.add_get('/users/{id}/visits', user_visits)
app.router.add_get('/locations/{id}', locations)
app.router.add_get('/visits/{id}', visits)

app.router.add_post('/users/{id}', users_update)
app.router.add_post('/users/{id}/visits', user_visits_update)
app.router.add_post('/locations/{id}', locations_update)


web.run_app(app, host='127.0.0.1', port=8080)

