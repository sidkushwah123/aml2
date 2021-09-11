from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import VsUsers
from project_control.models import VsSystemSettings
from django.contrib.auth.models import User, Group
# Register your models here.
class VsUsersAdmin(admin.ModelAdmin):
    search_fields = ['user__username','name','Type','Contact_no','Other_Type']
    list_display = ('user','name','user_code','Type','DOJ','Contact_no','Zip_Code','Other_Type')
    list_filter = ('user',)
    readonly_fields = ["user_code"]

    # def has_add_permission(self, request, obj=None):
    #     return False

admin.site.register(VsUsers,VsUsersAdmin)
admin.site.unregister(Group)

get_system_info = VsSystemSettings.objects.all().first()

priject_title = 'Rated Me test'
if get_system_info:
	if get_system_info.Project_Title:
		priject_title = get_system_info.Project_Title

admin.site.site_header = priject_title+' admin console'
admin.site.site_title = priject_title+' admin console'
admin.site.index_title = priject_title+' administration'
