from django.contrib import admin
from .models import VsSystemSettings
from import_export.admin import ImportExportModelAdmin
# Register your models here.
class VsSystemSettingsAdmin(ImportExportModelAdmin):
    list_display = ('Project_Title','Tag_Line','No_of_videos_watch_befure_login','No_of_videos_watch_after_login','No_of_videos_uploaded_by_one_account','Promotional_Email','Promotional_Email_password','Created_date','Updated_date')

    def has_add_permission(self, request):
        return False
    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(VsSystemSettings,VsSystemSettingsAdmin)
