from django.contrib import admin
from .models import License, Collection, PublicationType, Publication, PublicationAuthor,AuthorRank

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
    list_display = ['id', 'collection', 'publication_type', 'license', 'title']
    list_display_links = ['title',]
    search_fields = ['title',]

class AuthorRankAdmin(admin.ModelAdmin):
    list_display = ['name',]

class PublicationAuthorsAdmin(admin.ModelAdmin):
    list_display = ['publication_id','author_rank']

admin.site.register(Collection, LicenceAdmin)
admin.site.register(License, LicenceAdmin)
admin.site.register(PublicationType, PublicationTypeAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(AuthorRank,AuthorRankAdmin)
admin.site.register(PublicationAuthor, PublicationAuthorsAdmin)