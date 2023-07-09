from django.contrib import admin
from .models import Event, News
# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ['id','name','start_date','end_date','meeting_type','venue','start_time']

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'tag_name']

admin.site.register(Event, EventAdmin)
admin.site.register(News, NewsAdmin)
