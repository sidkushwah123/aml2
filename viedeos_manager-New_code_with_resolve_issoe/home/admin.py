from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import VsHomePageSettings
# Register your models here.
class VsHomePageSettingsAdmin(ImportExportModelAdmin):
    list_display = ('Video_Of_The_Day','Session_2_Title','Session_3_box_1_Title','Session_3_box_2_Title','Session_3_box_3_Title','Updated_date')


    # def has_add_permission(self, request):
    #     return False
    # # This will help you to disable delete functionaliyt
    # def has_delete_permission(self, request, obj=None):
    #     return False
admin.site.register(VsHomePageSettings,VsHomePageSettingsAdmin)
