#!flask/bin/python
import json
from flask import Flask, jsonify, Response, request
from markupsafe import escape

app = Flask(__name__)
db = dict()

@app.errorhandler(404)
def not_found(error):
    return Response(status=405)


@app.route('/hello', methods=['GET'])
def get_hello():
    return Response(response="HSE One Love!\n", status=200, mimetype="text/plain")


@app.route('/set', methods=['POST'])
def set_pair():
    if request.content_type != "application/json":
        return Response(status=415)
    
    if not request.json or not "key" in request.json or not "value" in request.json:
        return Response(status=400)
    
    db[request.json['key']] = request.json['value']
    return Response(status=200)


@app.route('/get/<string:key>', methods=['GET'])
def get_pair(key):
    if str(key) not in db:
        return Response(status=404)

    return Response(response=json.dumps({'key': key, 'value': db[key]}), status=200, mimetype="application/json")


def isnumber(x):
    return isinstance(x, (float, int))


@app.route('/divide', methods=['POST'])
def divide():
    if request.content_type != "application/json":
        return Response(status=415)
    
    if not request.json or not "dividend" in request.json or not "divider" in request.json or not isnumber(request.json["dividend"]) or not isnumber(request.json["divider"]) or request.json["divider"] == 0:
        return Response(status=400)
    
    return Response(response=str(request.json["dividend"] / request.json["divider"]), status=200, mimetype="text/plain")


if __name__ == '__main__':
    app.run(debug=True)