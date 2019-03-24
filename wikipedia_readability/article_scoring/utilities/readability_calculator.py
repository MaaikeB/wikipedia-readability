import readability

from article_scoring import keys



def get_readability_scores(text_extracts, readability_formulas=['FleschReadingEase']):
    """
    Gets the readability scores of the page extracts through the readibility library, which uses multiple readability
    metrics (amongst other the Coleman–Liau, Gunning fog, and Dale–Chall formulas)

    :param text_extracts (list): List of dicts with the following values: 'id' and 'text'
    :param readability_formulas (list): List of the readability formulas to get the scores for

    :return (dict): Dict with ids as the key and a dict as the value, with all the requested readability formulas
    and their score, so for example:
    {
        1234: {
            'FleschReadingEase': 99,
            'FunkyReadabilityFormula': 78
        },
        6372: {
            'FleschReadingEase': 99,
            'FunkyReadabilityFormula': 78
        },
    }
    """

    page_scores = {}

    # Loop over the page extracts and add the readability_scores to the dict
    for page_extract in text_extracts:

        # Skip the text in case there are not enough characters to validate it
        page_extract_text = page_extract[keys.ReadabilityCalculator.text]
        if len(page_extract_text) < 100:
            continue

        id = page_extract[keys.ReadabilityCalculator.id]
        page_scores[id] = {}

        # Call the readability library to get the scores
        readability_scores = readability.getmeasures(page_extract_text, lang='en')[keys.ReadabilityCalculator.readability_grades]

        for readability_formula in readability_formulas:
            # TODO: add try, catch ValueError and raise an Exception
            page_scores[id][readability_formula] = readability_scores[readability_formula]

    return page_scores