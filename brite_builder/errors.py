from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import RequestContext

def handler404(request):
    response = render_to_response('site/errors/404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('site/errors/500.html', {})
    response.status_code = 500
    return response