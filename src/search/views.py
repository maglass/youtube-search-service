import json
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

_API_GATEWAY_URL = 'https://n7blif15e6.execute-api.ap-northeast-2.amazonaws.com/develop-stage/yt/'


def _get_url(query, start, number):
    return '{}?query={}&start={}&number={}'.format(_API_GATEWAY_URL, query, start, number)


@csrf_exempt
def search(request):
    params = request.GET
    query = params.get('q')
    start = params.get('s', 0)
    number = params.get('n', 10)
    rr = requests.get(_get_url(query, start, number))
    content = rr.json()
    return HttpResponse(json.dumps(content['body']), content_type='application/json')
