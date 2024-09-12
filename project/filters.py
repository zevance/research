from django.db.models import QuerySet

class ProjectQuerySet(QuerySet):
	
    def search(sef, *kwargs):
        qs = self
        if kwargs.get('q', ''):
            qs = qs.filter(name__icontains=kwargs['q'])
        if kwargs.get('country', ''):
            qs = qs.filter(country=kwargs['country'])
        if kwargs.get('year', ''):
            qs = qs.filter(year=kwargs['year'])
        if kwargs.get('project_status', ''):
            qs = qs.filter(project_status=kwargs['project_status'])
        if kwargs.get('project_type', ''):
            qs = qs.filter(project_type=kwargs['project_type'])
        return qs