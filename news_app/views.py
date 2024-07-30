from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import NewsHistory
from .serializers import NewsHistorySerializer
from rest_framework.pagination import PageNumberPagination
import requests
from django.utils import timezone

class FetchTopNewsView(APIView):
    def get(self, request):
        keyword = request.query_params.get('keyword')
        category = request.query_params.get('category')
        country = request.query_params.get('country')


        url = f'https://newsapi.org/v2/top-headlines?apiKey={settings.NEWS_API_KEY}'
        if keyword:
            url += f'&q={keyword}'
        if category:
            url += f'&category={category}'
        if country:
            url += f'&country={country}'

        response = requests.get(url)
        data = response.json()
        
        if data.get('status') != 'ok':
            return Response({'error': 'Error fetching news'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        articles = data.get('articles', [])

        for article in articles:
            news_history, created = NewsHistory.objects.update_or_create(
                url=article.get('url'),
                defaults={
                    'keyword': keyword,
                    'category': category,
                    'country': country,
                    'source': article.get('source', {}).get('name'),
                    'author': article.get('author'),
                    'title': article.get('title'),
                    'description': article.get('description'),
                    'urlToImage': article.get('urlToImage'),
                    'publishedAt': article.get('publishedAt'),
                    'content': article.get('content'),
                    'fetched_at': timezone.now()
                }
            )

        return Response(data['articles'], status=status.HTTP_200_OK)

class FetchHistoryView(APIView):
    def get(self, request):
        history = NewsHistory.objects.all().order_by('-fetched_at')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(history, request)
        serializer = NewsHistorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    