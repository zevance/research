from django.contrib import admin
from .models import Event, News
# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'tag_name']

admin.site.register(Event)
admin.site.register(News, NewsAdmin)