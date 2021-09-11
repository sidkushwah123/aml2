from django.contrib import admin
from .models import VsCmsPage
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class VsCmsPageAdmin(ImportExportModelAdmin,SummernoteModelAdmin):
    summernote_fields = ('Page_content',)
    list_display = ('Title','keyword','Background_Image','Description','set_order')

    # def has_add_permission(self, request, obj=None):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False
admin.site.register(VsCmsPage,VsCmsPageAdmin)
