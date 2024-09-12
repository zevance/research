from django.db.models import QuerySet

class InnovationQuerySet(QuerySet):
	
    def search(sef, *kwargs):
        qs = self
        if kwargs.get('q', ''):
            qs = qs.filter(title__icontains=kwargs['q'])
        if kwargs.get('year', ''):
            qs = qs.filter(year_of_innovation=kwargs['year'])
        return qs