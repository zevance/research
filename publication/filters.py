from django.db.models import QuerySet

class PublicationQuerySet(QuerySet):
	
    def search(sef, *kwargs):
        qs = self
        if kwargs.get('q', ''):
            qs = qs.filter(title__icontains=kwargs['q'])
        if kwargs.get('year', ''):
            qs = qs.filter(year_of_publication=kwargs['year'])
        if kwargs.get('collection', ''):
            qs = qs.filter(collection=kwargs['collection'])
        if kwargs.get('publication_type', ''):
            qs = qs.filter(publication_type=kwargs['publication_type'])
 
        return qs