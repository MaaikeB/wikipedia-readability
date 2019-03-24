import json

from django.http import HttpResponse
from django.template import loader

from article_scoring import mediawiki_api


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

    # Get the category title from the request object, and perform basic validation
    category_title = request.GET['category_title']

    # todo validate that it is a string and no longer than 250 characters

    # Get the extracts of the category pages
    category_page_extracts = mediawiki_api.get_category_page_extracts(category_title, page_intro=True)

    response_data = {
        'category_page_extracts': category_page_extracts
    }

    # todo: Pass the list of page extracts to the readability calculator to get the readability scores for each

    return HttpResponse(json.dumps(response_data), content_type='application/json')