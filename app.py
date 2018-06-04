from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.TestDB


@app.route('/poster', methods=['GET'])
def get_all_posters():
    collection = db.FirstCollection
    output = []

    for q in collection.find():
        output.append({'name': q['name'], 'url': q['url']})

    return jsonify('result', output)


@app.route('/poster/<name>', methods=['GET'])
def get_poster_by_name(name):
    collection = db.FirstCollection
    q = collection.find_one({'name': name})

    if q:
        output = {'name': q['name'], 'url': q['url']}
    else:
        output = 'No results found'

    return jsonify('result', output)


@app.route('/poster', methods=['POST'])
def add_poster():
    collection = db.FirstCollection
    name = request.json['name']
    url = request.json['url']

    poster_id = collection.insert({'name': name, 'url': url})
    new_poster = collection.find_one({'_id': poster_id})

    output = {'name': new_poster['name'], 'url': new_poster['url']}
    return jsonify('result', output)


if __name__ == '__main__':
    app.run(debug=True)
