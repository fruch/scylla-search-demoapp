from sanic import Sanic
from sanic.response import json

app = Sanic("App Name")

app.static('/', './index.html', content_type="text/html; charset=utf-8")
app.static('/images', './images')
app.static('/style.css', './style.css')


movies = [
dict(id="1234", label="Ninja", value="Ninja"),
dict(id="1234", label="Home Alone", value="Home Alone"),
dict(id="1234", label="Lord of the Rings", value="Lord of the Rings"),
dict(id="1234", label="Snitch", value="Snitch"),
dict(id="1234", label="Good morning Vietnam", value="Good morning Vietnam"),
]

@app.route("/search")
async def test(request):
    term = request.args['term'][0]
    return json([m for m in movies if term.lower() in m['label'].lower()])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
