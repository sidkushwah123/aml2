from django.contrib import admin
from .models import VsUserSubscriptionPayment,VsSubscription,VsPayPal
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class VsUserSubscriptionPaymentAdmin(ImportExportModelAdmin):
    list_display = ('order_id','Descount_coupon','Package_name','Upload_Video_limit','User','Buy_date','Start_date','Expayer_date','Payment_status','Active_status','Amount','Amount_after_descount','Payment_method','Transaction_id')
    list_filter = ('Descount_coupon','User')
admin.site.register(VsUserSubscriptionPayment,VsUserSubscriptionPaymentAdmin)

class VsSubscriptionAdmin(ImportExportModelAdmin,SummernoteModelAdmin):
    summernote_fields = ('Description',)
    list_display = ('Package_name','Price','Upload_Video_limit','Set_order')

    def has_add_permission(self, request):
        return False
    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(VsSubscription,VsSubscriptionAdmin)


class VsPayPalAdmin(ImportExportModelAdmin):
    list_display = ('PayPal_Clientid','update_date')

    def has_add_permission(self, request):
        return False
    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(VsPayPal,VsPayPalAdmin)