from django.contrib import admin
from .models import User, Profile
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display =['id','first_name','username','last_name','email']
    list_display_links = ['first_name','username','last_name','email']
    search_fields = ['username','email']

class ProfileAdmin(admin.ModelAdmin):
    list_display =['id','specialization','specialization','qualification']
    list_display_links = ['specialization','specialization']
    search_fields = ['specialization',]

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)