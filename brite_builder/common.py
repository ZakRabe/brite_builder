import json
def get_post_json(request):
    return json.loads(request.body)