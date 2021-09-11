from django.contrib import admin
from .models import VsFavourite,VsSendEmailForNewVideo
from import_export.admin import ImportExportModelAdmin
# Register your models here.
class VsFavouriteAdmin(ImportExportModelAdmin):
    list_display = ('Subscribe','VsUser','Video','Create_date')
    list_filter = ('Subscribe','VsUser')
admin.site.register(VsFavourite,VsFavouriteAdmin)


class SendEmailForNewVideoAdmin(ImportExportModelAdmin):
    list_display = ('Videos','VsUser','Send_date')
    list_filter = ('Videos','VsUser')
admin.site.register(VsSendEmailForNewVideo,SendEmailForNewVideoAdmin)