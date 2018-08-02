from datetime import datetime
from elasticsearch import Elasticsearch
from pymongo import MongoClient

client = MongoClient()
db = client.pixiv
collection = db.illust
es = Elasticsearch()

result = collection.find().limit(10)
for img in result:
    dec = int(img['image_hash'], 16);
    doc = {
        'id': int(img['illust_id']),
        'hash': bin(dec)[2::],
        'created_at': img['created_at'],
    }
    res = es.index(index="pixiv", doc_type='pixiv', id=int(img['illust_id']), body=doc)
    print(res['result'])

es.indices.refresh(index="pixiv")
