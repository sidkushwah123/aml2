from django.contrib import admin
from .models import VsVideos,VsComments,VsRating,VsNonRegisterUser
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
class VsVideosAdmin(SummernoteModelAdmin):
    search_fields = ['Videos_Title','Videos_id']
    summernote_fields = ('Description',)
    list_display = ('Videos_Title','Videos_id','Videos_Slug','Categoryes','Sub_Categoryes','Country','Publich_Status','Meta_Title','Meta_keyword','Views','Created_date','Created_By','Updated_date','mail_send_status')
    list_filter = ('Categoryes','Sub_Categoryes','Created_By','Created_date',)
    readonly_fields = ["Videos_id"]
admin.site.register(VsVideos,VsVideosAdmin)


class VsCommentsAdmin(ImportExportModelAdmin):
    list_display = ('Video','User','Comment','Status','Created_date','Updated_date')
    list_filter = ('Created_date',)
admin.site.register(VsComments,VsCommentsAdmin)

class VsReatingAdmin(ImportExportModelAdmin):
    search_fields = ['Video']
    list_display = ('Video','User','Reating_attrbute','Reating','Status','Created_date','Updated_date')
    list_filter = ('Created_date','Reating_attrbute','Status','User',)
admin.site.register(VsRating,VsReatingAdmin)


class VsNonRegisterUserAdmin(ImportExportModelAdmin):
    list_display = ('user_id','Video','watch_date','User_ip')
    list_filter = ('watch_date','User_ip',)
admin.site.register(VsNonRegisterUser,VsNonRegisterUserAdmin)