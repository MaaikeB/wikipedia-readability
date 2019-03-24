import json

from django.http import HttpResponse
from django.template import loader

from article_scoring.utilities import mediawiki_api
from article_scoring.utilities import readability_calculator
from article_scoring import errors
from article_scoring import keys



def index(request):
    """
    Renders the index HTML page with the categories form

    :param request(WSGIRequest): The WSGI Request object
    :return: HTTPResponse with the rendered HTML page
    """

    template = loader.get_template('article_scoring/index.html')
    return HttpResponse(template.render({}, request))


def get_articles_in_category(request):
    """
    Gets a list of articles for the chosen category sorted by readability score.

    :param request (WSGIRequest): The WSGI Request object, which includes the category the user chose to get articles for
    :return (HttpResponse): An HttpResponse with JSON data, that includes a list of articles with title and readability score
    """

    # Get the category title from the request object, and perform basic validation
    # TODO: Validate that the category_title parameter is sent, that it is a string and no longer than 250 characters
    category_title = request.GET['category_title']

    # Get the extracts of the category pages
    category_page_extracts = mediawiki_api.get_category_page_extracts(category_title, page_intro=True)

    # If there are no page extracts, return a response with an error
    if (len(category_page_extracts) == 0):
        response_data = {
            keys.API.error: errors.MediaWiki.NoCategoryMembers
        }
        return HttpResponse(json.dumps(response_data), content_type='application/json')

    # Get the page readability scores
    # Prepare list with 'generic' keys in order to send it to the readability calculator
    text_list = []
    for category_page_extract in category_page_extracts:
        text_list.append({
            keys.ReadabilityCalculator.id: category_page_extract[keys.MediaWikiAPI.page_id],
            keys.ReadabilityCalculator.text: category_page_extract[keys.MediaWikiAPI.extract]
        })

    readability_scores = readability_calculator.get_readability_scores(text_list)

    # If there are no results, return a response with an error
    if (len(category_page_extracts) == 0):
        response_data = {
            keys.API.error: errors.MediaWiki.NoCategoryMembers
        }
        return HttpResponse(json.dumps(response_data), content_type='application/json')

    # Add the readability scores to the page_extracts list
    category_page_extracts_with_scores = []
    for index, category_page_extract in enumerate(category_page_extracts):
        page_id = category_page_extract[keys.MediaWikiAPI.page_id]

        try:
            page_readability_scores = readability_scores[page_id]
            category_page_extracts_with_scores.append(
                {**category_page_extracts[index], **{keys.GetArticlesInCategory.readability_scores: page_readability_scores}}
            )

        except KeyError:
            # If there is no readability score for the page, don't add it to the list
            pass

    # Sort the list according to least readable to most readable
    category_page_extracts_with_scores.sort(key=lambda x: x[keys.GetArticlesInCategory.readability_scores][keys.GetArticlesInCategory.flesch_reading_ease])

    # Prepare the response data
    response_data = {
        keys.GetArticlesInCategory.category_page_extracts: category_page_extracts_with_scores
    }

    return HttpResponse(json.dumps(response_data), content_type='application/json')