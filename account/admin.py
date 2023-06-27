from django.contrib import admin
from .models import User
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display =['id','first_name','username','last_name','email']
    list_display_links = ['first_name','username','last_name','email']
    search_fields = ['username','email']

admin.site.register(User, UserAdmin)