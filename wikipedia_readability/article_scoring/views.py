import json

from django.http import HttpResponse
from django.template import loader



def index(request):
    """
    Renders the index HTML page with the categories form

    :param request: The WSGI Request object
    :return: HTTPResponse with the rendered HTML page
    """

    template = loader.get_template('article_scoring/index.html')
    return HttpResponse(template.render({}, request))


def get_articles_in_category(request):
    """
    Gets a list of articles for the chosen category sorted by readability score.

    :param request: The WSGI Request object, which includes the category the user chose to get articles for
    :return (HttpResponse): An HttpResponse with JSON data, that includes a list of articles with title and readability score
    """

    response_data = {
        'wikipedia_articles': [
            {'title': 'some physics', 'readability_score': 23},
            {'title': 'some more physics', 'readability_score': 56},
            {'title': 'even more physics', 'readability_score': 99}
        ]
    }

    return HttpResponse(json.dumps(response_data), content_type='application/json')