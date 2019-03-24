
## VIEWS

class GetArticlesInCategory(object):
    readability_scores = 'readability_scores'
    flesch_reading_ease = 'FleschReadingEase'
    category_page_extracts = 'category_page_extracts'


## MODULES

class MediaWikiAPI(object):
    page_id = 'pageid'
    extract = 'extract'
    query = 'query'
    category_members = 'categorymembers'
    pages = 'pages'


class ReadabilityCalculator(object):
    id = 'id'
    text = 'text'
    readability_grades = 'readability grades'


## MISC

class API(object):
    error = 'error'