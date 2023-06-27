from django.contrib import admin
from project.models import Project

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title','total_value','project_status','project_type','project_pi','project_co_pi',
    'project_member','project_donor','project_partner']
    list_display_links =['title','project_type','project_pi']

admin.site.register(Project, ProjectAdmin)