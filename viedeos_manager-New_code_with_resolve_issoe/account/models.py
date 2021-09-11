from django.db import models
from django.contrib.auth.models import User
import django
from datetime import date
from django.db.models.signals import pre_save
from imratedme.utils import unique_id_generator_for_VsUsers
# Create your models here.

def user_directory_path_favicon(instance, filename):
    project_id_in_list = instance.name.split(" ")
    today_date = date.today()
    project_id_in_string = '_'.join([str(elem) for elem in project_id_in_list])
    return '{0}/{1}'.format("user_imsge/"+project_id_in_string+"/"+str(today_date.year)+"/"+str(today_date.month)+"/"+str(today_date.day),filename)

class VsUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    user_code = models.CharField(max_length=120,null=True,blank=True)
    name = models.CharField(max_length=20,default="User")
    Type = models.CharField(max_length=200,null=True,blank=True)
    Image  = models.FileField(upload_to=user_directory_path_favicon,null=True,blank=True)
    DOJ  = models.DateField(default=django.utils.timezone.now)
    status = models.BooleanField(default=True)
    Contact_no = models.BigIntegerField(default=0,null=True,blank=True)
    Zip_Code = models.IntegerField(null=True,blank=True)
    otp = models.CharField(null=True,blank=True,max_length=5)
    password = models.CharField(null=True,blank=True,max_length=120)
    Other_Type = models.CharField(null=True,blank=True,max_length=120)
    Site_Link = models.URLField(null=True,blank=True,max_length=120)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "VS Users"

def pre_save_create_user_code(sender, instance, *args, **kwargs):
    if not instance.user_code:
        instance.user_code= unique_id_generator_for_VsUsers(instance)
pre_save.connect(pre_save_create_user_code, sender=VsUsers)

