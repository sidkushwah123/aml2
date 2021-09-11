from django.contrib import admin
from .models import VsReatingAttribute,VsCategory,VsSubCategoryes,VsConnectReatingWithCate
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class LsCategoryesAdmin(ImportExportModelAdmin):
    search_fields = ['Title']
    # summernote_fields = ('description',)
    list_display = ('Title','Slug','Status','Created_date','Created_By')
    list_filter = ('Created_By',)
    readonly_fields = ["Slug"]
admin.site.register(VsCategory,LsCategoryesAdmin)

class VsSubCategoryesAdmin(ImportExportModelAdmin):
    search_fields = ['Title']
    # summernote_fields = ('description',)
    list_display = ('Category','Title','Slug','Status','Created_date','Created_By')
    list_filter = ('Created_By',)
    readonly_fields = ["Slug"]
admin.site.register(VsSubCategoryes,VsSubCategoryesAdmin)


class VsReatingAttributeAdmin(ImportExportModelAdmin,SummernoteModelAdmin):
    search_fields = ['Title']
    summernote_fields = ('Description',)
    list_display = ('Title','Slug','Status','Created_date','Created_By')
    list_filter = ('Created_By',)
    readonly_fields = ["Slug"]
admin.site.register(VsReatingAttribute,VsReatingAttributeAdmin)


class VsConnectReatingWithCateAdmin(ImportExportModelAdmin):
    search_fields = ['Title']
    list_display = ('Category','Sub_Category','Created_date','Created_By')
    list_filter = ('Category','Sub_Category',)
admin.site.register(VsConnectReatingWithCate,VsConnectReatingWithCateAdmin)