from django.urls import path
from .views import FetchTopNewsView, FetchHistoryView

urlpatterns = [
    path('fetch-topnews/', FetchTopNewsView.as_view(), name='fetch-news'),
    path('fetch-history/', FetchHistoryView.as_view(), name='fetch-history'),
    
]
