from django.contrib import admin
from .models import Project,Donor, Partner,Member, Role
# Register your models here.
class DonorsAdmin(admin.ModelAdmin):
    list_display = ['name','email','contact_address','contact_number','country','description']
    search_fields = ['name','country']

class PartnersAdmin(admin.ModelAdmin):
    list_display = ['name',]
    search_fields = ['name',]

class RolesAdmin(admin.ModelAdmin):
    list_display = ['name',]
    search_fields = ['name',]

class MembersAdmin(admin.ModelAdmin):
    list_display = ['title', 'first_name','last_name']
    search_fields =['first_name', 'last_name']

    # def get_roles(self, obj):
    #     return "\n".join([r.role for r in obj.roles.all()])

class ProjectsAdmin(admin.ModelAdmin):
    list_display = ['title','description']
    search_fields = ['donor','partner','title', 'member']

    # def get_donors(self, obj):
    #     return "\n".join([d.donor for d in obj.donors.all()])

    # def get_partners(self, obj):
    #     return "\n".join([p.partner for p in obj.partners.all()])

    # def get_members(self, obj):
    #     return "\n".join([m.member for m in obj.members.all()])

admin.site.register(Project, ProjectsAdmin)
admin.site.register(Donor, DonorsAdmin)
admin.site.register(Partner, PartnersAdmin)
admin.site.register(Member, MembersAdmin)
admin.site.register(Role, RolesAdmin)