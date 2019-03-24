import json
import requests

from article_scoring import keys



WIKIPEDIA_API_BASE_URL = 'https://en.wikipedia.org/w/api.php?'


def get_category_page_extracts(category_title, articles_limit=50, page_intro=True, number_of_characters=100):
    """
    Gets the page extracts from the given category

    :param category_title (string): The title of the category to retrieve the extracts for
    :param articles_limit (integer): The maximum amount of articles to retrieve, by default 50
    :param page_into (boolean): Whether or not to get only the Wikipedia page intro
    :param number_of_characters: The amount of characters to return for each Wikipedia page. This parameter should not be
    passed when passing page_intro=True
    :return (list): A list of dict objects representing the pages with the following properties:
    - id
    - extract
    """

    # TODO: Validate the parameters & raise Exceptions if invalid
    # - The category_title should be a string and no more than 250 characters
    # - The articles_limit should be an integer
    # - If page_intro is True, the number_of_characters parameter should not be sent
    # - The page_intro should be a Boolean
    # - The number of characters should be an integer

    # Get the category page ids
    category_page_ids = _get_category_page_ids(category_title, articles_limit)

    # If there are no page ids, return an empty list
    if len(category_page_ids) == 0:
        return []

    # Get the extracts of the pages
    page_extracts = _get_page_extracts(category_page_ids, page_intro, number_of_characters)

    # Return the extracts of the pages
    return page_extracts



def _get_category_page_ids(category_title, articles_limit):
    """
    Gets the first batch of article ids in a certain category

    :param category_title (string): The title of the category to retrieve the article ids for
    :param articles_limit (integer): The maximum amount of articles to retrieve
    :return (list): List of page ids (integers)
    """

    # Make the API call
    url = WIKIPEDIA_API_BASE_URL + 'format=json&action=query&list=categorymembers&cmtype=page&prop=iwlinks&' \
          'cmtitle=Category:' + category_title + '&' \
          'cmlimit=' + str(articles_limit)

    response = requests.get(url)

    # Do some basic checks on the response - status code
    if (response.status_code != 200):
        return []

    # Get the response data and decode it
    response_data = response.content.decode('utf8')

    # Create a dict object from the JSON
    response_data = json.loads(response_data)

    # Extract the page ids from the list of objects. Catch an ValueError in case the expected properties are not present
    try:
        category_page_list = response_data[keys.MediaWikiAPI.query][keys.MediaWikiAPI.category_members]
        page_ids = [category_page[keys.MediaWikiAPI.page_id] for category_page in category_page_list]

    except ValueError:
        return []

    # Return the list of page ids
    return page_ids



def _get_page_extracts(page_ids, page_intro, number_of_characters):
    """
    Gets text extracts for Wikipedia pages with certain page ids.
    By default only the page intro will be retrieved, but alternatively when passing the number_of_characters parameter,
    a specific amount of characters (starting from the start of the article) will be returned.

    :param page_ids (list): List of page ids (integers) to retrieve the extracts for. This list should be no longer than 50.
    :param page_intro (boolean): Whether or not to get only the Wikipedia page intro
    :param number_of_characters: The amount of characters to return for each Wikipedia page
    :return: A list with dicts - each representing a Wikipedia page extract - with the following properties:
    ..., ...
    """

    # TODO: Validate that the page_ids list is no longer than 50 & raise Exception if this is not the case

    # Prepare the page_intro or number_of_characters parameters
    page_intro_param = ''
    number_of_characters_param = ''
    if (page_intro is not None):
        page_intro_param = 'exintro=true&'

    else:
        number_of_characters_param = 'exchars=' + number_of_characters + '&'

    # Transform the list of page ids into a string that includes all the ids, separated with |
    category_page_ids_string = "|".join(str(page_id) for page_id in page_ids)

    # Make the API call
    url = WIKIPEDIA_API_BASE_URL + 'format=json&action=query&prop=extracts&explaintext=true&' + \
                                    page_intro_param + \
                                    number_of_characters_param + \
                                   'pageids=' + category_page_ids_string

    response = requests.get(url)

    # Do a basic check on the response - the status code should be 200
    if (response.status_code != 200):
        return []

    # Decode the response data
    response_data = response.content.decode('utf8')

    # Load the object from the JSON
    response_data = json.loads(response_data)

    # Get the 'pages' object
    # TODO: Add try and raise Exception in case of a KeyError
    page_data = response_data[keys.MediaWikiAPI.query][keys.MediaWikiAPI.pages]

    # Create a list from the dict, and add only page objects that have extract and id properties
    page_list = []
    for page, page_dict in page_data.items():
        if ('extract' in page_dict and 'pageid' in page_dict):
            page_list.append(page_dict)

    return page_list