from flask import render_template
from flask import Flask
from pymongo import MongoClient
from flask import send_from_directory, request
from flask_paginate import Pagination
import pymongo

app = Flask(__name__)


@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    client = MongoClient()
    db = client.pixiv
    collection = db.illust

    collection.find()

    data = collection.find().sort([("bookmark", pymongo.DESCENDING)]).skip(10 * (page -1)).limit(10)
    count = collection.find().count()
    pagination = Pagination(page=page, total=count, css_framework='bootstrap4')
    return render_template('index.html', images=data, pagination=pagination)


@app.route('/image/<path:filename>')
def image(filename):
    return send_from_directory('path', filename)


@app.route('/search')
def search():
    tag = request.args.get('tags')
    client = MongoClient()
    db = client.pixiv
    collection = db.illust_tags

    result = collection.find({"tag": {"$regex": ".*" + tag + ".*"}}).skip(0).limit(10)
    count = collection.find({"tag": {"$regex": ".*" + tag + ".*"}}).count()
    illust_ids = [o['illust_id'] for o in result]

    data = db.illust.find({"illust_id": {"$in": illust_ids}}).skip(0).limit(10)
    pagination = Pagination(page=0, total=count, css_framework='bootstrap4')
    return render_template('index.html', images=data, pagination=pagination)


if __name__ == '__main__':
    app.run()

