from django.contrib import admin
from .models import Donor, Project

# Register your models here.
class DonorAdmin(admin.ModelAdmin):
    list_display =['id','name','email','contact_address','contact_number','country','description']
    search_fields = ['name',]
    list_display_links = ['name',]
    
class ProjectAdmin(admin.ModelAdmin):
    list_display =['id','title']
    search_fields = ['title',]
    list_display_links = ['title',]

admin.site.register(Donor, DonorAdmin)
admin.site.register(Project, ProjectAdmin)
