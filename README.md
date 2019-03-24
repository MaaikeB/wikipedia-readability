# Wikipedia Article Readability


## Description

This app shows Wikipedia articles in a certain category, while giving a certain score for the readability.
The user enters a category, for example 'physics' and a list of articles in that category will be presented.
The list will be sorted by readability - from least readable to most readable.

Readibility can be defined in a number of ways, this App uses the Flesch–Kincaid readability test, 
see for more information: https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests

## Install the project

Download/clone the project.

Create a virtualenv at the root of the project and activate it.
```
mkdir venv
python3 -m virtualenv venv
source venv/bin/activate
```

Install the requirements:
```
pip install -r requirements.txt
```

## Run the project

```
python manage.py runserver
```

Now browse to: http://127.0.0.1:8000/article_scoring/

