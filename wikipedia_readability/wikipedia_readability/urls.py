from django.urls import include, path

urlpatterns = [
    path('article_scoring/', include('article_scoring.urls')),
]