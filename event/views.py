from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import EventsSerializer, NewsSerializer
from .models import Event,News
from django.views.generic import ListView,DetailView
from rest_framework import generics

# Create your views here.
class NewsListView(ListView):
    template_name = 'core/news.html'
    model = News
    paginate_by = 8

news_list_view = NewsListView.as_view()

def news_details_view(request, pk):
    news = get_object_or_404(News, id=pk)
    latestNews = News.objects.exclude(id=pk).order_by('-created_at')[:5]
    context = {
        'news' : news,
        'latestNews': latestNews,
    }
    return render(request, 'core/news_details.html', context)

#API VIEWS
class EventsListView(APIView):
    def get(self, request, *args, **kwargs):
        instance = Event.objects.all()
        data = {}
        if instance:
            data = EventsSerializer(instance, many = True).data
        return Response(data)

events_list_api_view = EventsListView.as_view()

class EventDetailsAPIView(APIView):
    def get_object(self, pk):
        try:
            return Event.objects.get(id =pk)
        except Event.DoesNotExist:
            return Response('Event does not exist...!!!!')
        
    def get(self, request, pk):
        event = self.get_object(pk)
        serializer = EventsSerializer(event, many=False)
        return Response(serializer.data)

event_details_api_view = EventDetailsAPIView.as_view()

class NewsListAPIView(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer