import json
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

_SEARCH_API_HOST = 'http://13.125.252.81:9200'
_INDEX_NAME = 'collection-final'


@csrf_exempt
def search(request):
    params = request.GET
    query = params.get('q')
    start = params.get('s', 0)
    number = params.get('n', 10)

    contents = _search(query, start, number)
    documents = _get_documents(contents)
    response = dict()
    response['documents'] = documents
    return HttpResponse(json.dumps(response), content_type='application/json')


def _search(query, start, number):
    headers = {'Content-Type': 'application/json'}
    params = _get_params(query, start, number)
    data = json.dumps(params)
    rr = requests.get(_get_search_url(), headers=headers, data=data)

    content = rr.json()
    return content


def _get_documents(contents):
    if 'hits' not in contents:
        return list()
    hits = contents['hits']['hits']

    documents = list()
    for hh in hits:
        source = hh['_source']
        channel_id = source['channel_id']
        channel_name = source['channel_name']
        video_id = source['video_id']
        title = source['title']
        views = source['views']
        rating = source['rating']
        description = source['summary']

        doc = dict()
        doc['channel_id'] = channel_id
        doc['channel_name'] = channel_name
        doc['video_id'] = video_id
        doc['title'] = title
        doc['views'] = views
        doc['rating'] = rating
        doc['summary'] = description
        documents.append(doc)
    return documents


def _get_search_url():
    return '{}/{}/_search'.format(_SEARCH_API_HOST, _INDEX_NAME)


def _get_params(query, start, number):
    return {
        'from': start,
        'size': number,
        "query": {
            "function_score": {
                "query": {
                    "multi_match": {
                        "query": query,
                        "operator": "and",
                        "fields": ["title_indices", "desc_indices"]
                    }},
                "boost_mode": "replace",
                "score_mode": "sum",
                "functions": [
                    {
                        "filter": {
                            "match": {
                                "title_indices": {"query": query, "operator": "and"}
                            }
                        },
                        "weight": 0.7
                    },
                    {
                        "filter": {
                            "match": {
                                "desc_indices": {"query": query, "operator": "and"}
                            }
                        },
                        "weight": 0.3
                    },
                    {
                        "script_score": {
                            "script": {
                                "source": "doc['caption_quality'].value"
                            }
                        },
                        "weight": 0.2
                    },
                    {
                        "script_score": {
                            "script": {
                                "source": "doc['image_quality'].value"
                            }
                        },
                        "weight": 0.1
                    }
                ]
            }
        }
    }
