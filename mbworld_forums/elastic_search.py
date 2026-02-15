"""
Installation: https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html

Tutorial :https://medium.com/analytics-vidhya/quick-start-elasticsearch-with-python-a2578cd87339
https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html#install-deb
"""

from elasticsearch import Elasticsearch, helpers


class ElasticSearchConfig:
    _doc_type = "threads"
    # index = "forum-name"

    def __init__(self, forum_index):
        super().__init__()
        self.index = forum_index
        self.es = Elasticsearch(ES_HOST="http://localhost", ES_PORT=9200)
        self.create_index()

    def insert_bulk(self, posts):
        if not posts:
            return
        res = helpers.bulk(self.es, posts)
        print(f"{res[0]} posts inserted into Elastic Search")

    def create_index(self):
        self.es.indices.create(index=self.index, ignore=400)

    def insert_item(self, item):
        res = self.es.index(index=self.index, id=item['message_id'], body=item)
        print(f"Post {res['result']} with message id {'message_id'}")

    def update(self, item, _id):
        res = self.es.update(index=self.index, id=_id, body=item)
        print(res)

    def get_document(self, _id):
        print(self.es.get(index=self.index, id=_id)['_source'])

    def delete(self, _id):
        res = self.es.delete(index=self.index, id=_id)
        print(res)
