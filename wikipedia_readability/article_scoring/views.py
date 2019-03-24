from django.http import HttpResponse
from django.template import loader



def index(request):
    """
    Returns the index HTML page with the categories form

    :param request: The WSGI Request object
    :return: HTTPRespone with the rendered HTML page
    """

    template = loader.get_template('article_scoring/index.html')
    return HttpResponse(template.render({}, request))