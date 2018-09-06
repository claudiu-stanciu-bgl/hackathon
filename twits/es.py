import os

from elasticsearch import Elasticsearch


class ESClient(object):
    ES_HOST = os.environ.get('ES_HOST',
                             'https://search-data-insight-p6k37focny45vkoxg62ikpduli.eu-west-1.es.amazonaws.com/')
    ES_PORT = int(os.environ.get('ES_PORT', '443'))
    ES_INDEX = os.environ.get('ES_INDEX', 'twits')

    es = Elasticsearch([ES_HOST],
                       port=ES_PORT,
                       use_ssl=True)

    def insert_entry(self, data):
        self.es.index(index=self.ES_INDEX, doc_type='twit', body=data)

    def create_index(self):
        request_body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            },

            'mappings': {
                'the_tweets': {
                    'properties': {
                        'author_weighting': {'type': 'text'},
                        'emotions': {'type': 'nested'},
                        'keywords': {'type': 'nested'},
                        'raw_test': {'type': 'text'},
                        'timestamp': {'type': 'date'}

                    }}}
        }
        self.es.indices.create(index=self.ES_INDEX, body=request_body)
        print("created index " + self.ES_INDEX)
    def delete_index(self):
        self.es.indices.delete(index=self.ES_INDEX)
        print("deleted index " + self.ES_INDEX)


esclient = ESClient()
# esclient.create_index()
# esclient.delete_index()
