from django.shortcuts import render
from django.views.generic import TemplateView
import requests
import json
from django.http import JsonResponse
from rest_framework.response import Response

# Create your views here.
class DashboardPageView(TemplateView):
    template_name ='research/dashboard.html'

dashboard_view = DashboardPageView.as_view()

class UploadPublicationPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'research/add-publication.html')

    def post(self, request, *args, **kwargs):
        doi = request.POST.get('doi')
        if doi:
            url = f'https://api.crossref.org/works/{doi}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                publication = {
                    'type': data['message']['type'],
                    'title': data['message']['title'][0],
                    'author_1': data['message']['author'][0]['given'] + ' ' + data['message']['author'][0]['family'],
                    'author_2': data['message']['author'][1]['given'] + ' ' + data['message']['author'][1]['family'],
                    'author_3': data['message']['author'][2]['given'] + ' ' + data['message']['author'][2]['family'],
                    #'authors': [author['given'] + ' ' + author['family'] for author in data['message']['author']],
                    'journal': data['message']['container-title'][0],
                    'abstract': data['message']['abstract'],
                    'year': data['message']['issued']['date-parts'][0][0],
                    'volume': data['message']['volume'],
                    # 'issue': data['message']['issue'],
                    'pages': data['message']['page'],
                    'publisher': data['message']['publisher'],
                    'doi': data['message']['DOI'],
                    # 'country': data['message']['country'],
                }
                return render(request, 'research/publication-detail.html', {'publication': publication})
            else:
                error_message = f"Error retrieving publication data for DOI {doi}."
        else:
            error_message = "DOI not provided."
        return render(request, 'research/add-publication.html', {'error_message': error_message})

add_publication_view = UploadPublicationPageView.as_view()