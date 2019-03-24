from django.urls import path

from . import views

urlpatterns = [
    # Page Views - returning rendered HTML
    path('', views.index, name='index'),

    # API Views - called by AJAX calls, returning JSON objects
    path('get_articles_in_category', views.get_articles_in_category, name='index'),

]