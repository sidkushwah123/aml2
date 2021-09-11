from django.db import models
from datetime import date
import django
from account.models import VsUsers
from django.db.models.signals import pre_save
from imratedme.utils import unique_id_generator_for_order_id
from manage_coupons.models import AwCuponCode
# Create your models here.


class VsPayPal(models.Model):
    PayPal_Clientid = models.CharField(max_length=500,help_text='IF you add sendbox Client_id then PayPal work as sendbox and if you add Live client_id then PayPal work as Live.')
    update_date = models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)
    def __str__(self):
        return str(self.PayPal_Clientid)
    class Meta:
        verbose_name_plural = "Vs PayPal"


class VsSubscription(models.Model):
    Package_name = models.CharField(max_length=500)
    Price = models.FloatField(default=0)
    Free_trial = models.BooleanField(default=False,help_text="one month free trial for first user")
    Upload_Video_limit = models.IntegerField(default=0)
    Description = models.TextField(null=True, blank=True)
    Set_order = models.IntegerField(default=0)

    def __str__(self):
        return str(self.Package_name)
    class Meta:
        verbose_name_plural = "VS Subscription"

class VsUserSubscriptionPayment(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    Package_name = models.ForeignKey(VsSubscription, on_delete=models.SET_NULL, null=True, blank=True, related_name="package_VsSubscription")
    Upload_Video_limit = models.IntegerField(default=0)
    User = models.ForeignKey(VsUsers, on_delete=models.SET_NULL, null=True, blank=True, related_name="User_VsUserSubscriptionPayment")
    Buy_date = models.DateTimeField(default=django.utils.timezone.now,null=True, blank=True)
    Start_date = models.DateTimeField(default=django.utils.timezone.now,null=True, blank=True)
    Expayer_date = models.DateTimeField(default=django.utils.timezone.now,null=True, blank=True)
    Payment_status = models.BooleanField(default=False)
    Active_status = models.BooleanField(default=False)
    Amount = models.FloatField(default=0)
    Descount_coupon  = models.ForeignKey(AwCuponCode, on_delete=models.SET_NULL, null=True, blank=True, related_name="Coupon_code_VsSubscription")
    Amount_after_descount = models.FloatField(default=0)
    Payment_method  = models.CharField(max_length=500,null=True, blank=True)
    Transaction_id = models.CharField(max_length=500,null=True, blank=True)


    def __str__(self):
        return str(self.order_id)
    class Meta:
        verbose_name_plural = "VS User Subscription Payment"

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id= unique_id_generator_for_order_id(instance)

pre_save.connect(pre_save_create_order_id, sender=VsUserSubscriptionPayment)