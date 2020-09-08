from sanic import Sanic
from sanic.response import json
from cassandra.cluster import Cluster
from aiocassandra import aiosession

app = Sanic("App Name")

app.static('/', './index.html', content_type="text/html; charset=utf-8")
app.static('/images', './images')
app.static('/style.css', './style.css')


@app.listener('before_server_start')
async def setup_db(app, loop):
    cluster = Cluster()
    app.session = cluster.connect()
    aiosession(app.session)
    app.query1 = app.session.prepare("SELECT * FROM keyspace1.movie_data WHERE primaryTitle LIKE ? LIMIT 20 ALLOW FILTERING ;")


@app.route("/search")
async def test(request):
    term = request.args['term'][0]
    results = await app.session.execute_future(app.query1, parameters=[f'{term}%'])
    return json([dict(id=row.tconst, label=row.originaltitle, value=row.originaltitle) for row in results])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
