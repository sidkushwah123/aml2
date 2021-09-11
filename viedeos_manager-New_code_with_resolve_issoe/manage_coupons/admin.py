from django.contrib import admin
from .models import AwCuponCode
from import_export.admin import ImportExportModelAdmin


# Register your models here.

class AwCuponCodeAdmin(ImportExportModelAdmin):
    list_display = ('CouponCode', 'Type', 'Amount', 'Usage_Limit_Per_Coupon', 'Usage_Limit_Per_User', 'Valid_from', 'Valid_to',
    'Status', 'created_date')
    readonly_fields = ["CouponCode"]


admin.site.register(AwCuponCode, AwCuponCodeAdmin)