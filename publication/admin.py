from django.contrib import admin
from .models import License, Collection, PublicationType, Publication, Innovation, InnovationMedia, Innovator

# Register your models here.
class LicenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name',]
    search_fields = ['name',]

class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name',]
    search_fields = ['name',]

class PublicationTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name',]
    search_fields = ['name',]

class PublicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'collection', 'publication_type', 'license', 'title','tags']
    list_display_links = ['title',]
    search_fields = ['title',]

class InnovationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'patent', 'year_of_innovation']
    list_display_links = ['title',]
    search_fields = ['title',]

class InnovationMediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'innovation', 'media']
    list_display_links = ['innovation',]
    search_fields = ['innovations',]

class InnovatorAdmin(admin.ModelAdmin):
    list_display = ['id', 'innovation', 'title', 'first_name', 'last_name']
    list_display_links = ['innovation',]
    search_fields = ['innovations',]


admin.site.register(Collection, LicenceAdmin)
admin.site.register(License, LicenceAdmin)
admin.site.register(PublicationType, PublicationTypeAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Innovation, InnovationAdmin)
admin.site.register(InnovationMedia, InnovationMediaAdmin)
admin.site.register(Innovator, InnovatorAdmin)