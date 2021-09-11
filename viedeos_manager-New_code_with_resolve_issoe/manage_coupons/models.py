from django.db import models
import django
from imratedme.utils import  unique_id_generator_for_CouponCode
from django.db.models.signals import pre_save
from django.urls import reverse
# Create your models here.
class AwCuponCode(models.Model):
    CouponCode = models.CharField(max_length=120, unique=True)
    Type = models.CharField(max_length=120,help_text="A for Amount & P for Percentage")
    Amount = models.FloatField(default=0)
    Usage_Limit_Per_Coupon = models.IntegerField(default=0)
    Usage_Limit_Per_User = models.IntegerField(default=0)
    Valid_from  = models.DateField()
    Valid_to  = models.DateField()
    Status = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=django.utils.timezone.now)


    def __str__(self):
        return self.CouponCode
    class Meta:
        verbose_name_plural = "LS Coupon Code"


    # def get_absolute_url(self):
    #     return reverse('admin_manage_cupon_code:admin_manage_cupon_code')

def pre_save_create_CouponCode(sender, instance, *args, **kwargs):
    if not instance.CouponCode:
        instance.CouponCode= unique_id_generator_for_CouponCode(instance)
pre_save.connect(pre_save_create_CouponCode, sender=AwCuponCode)
