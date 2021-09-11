from django.db import models
from account.models import VsUsers
from django.contrib.auth.models import User
import django
from django.db.models.signals import pre_save
from datetime import date
from imratedme.utils import slug_generator_for_category,slug_generator_for_sub_category,slug_generator_for_reating_review
# Cr
def user_directory_path_category_image(instance, filename):
    producer_id_in_list = instance.Title.split(" ")
    today_date = date.today()
    producer_id_in_string = '_'.join([str(elem) for elem in producer_id_in_list])
    return '{0}/{1}'.format("categoryes/"+producer_id_in_string+"/"+str(today_date.year)+"/"+str(today_date.month)+"/"+str(today_date.day),filename)




class VsCategory(models.Model):
    Title = models.CharField(max_length=120,unique=True)
    Image = models.ImageField(null=True,upload_to=user_directory_path_category_image,blank=True)
    Slug = models.CharField(max_length=120, null=True, blank=True)
    Status = models.BooleanField(default=True)
    Created_date = models.DateTimeField(default=django.utils.timezone.now)
    Created_By = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name="User_cate")


    def __str__(self):
        return self.Title
    class Meta:
        verbose_name_plural = "VS Category"

def pre_save_create_slug_for_cate(sender, instance, *args, **kwargs):
    if not instance.Slug:
        instance.Slug= slug_generator_for_category(instance)

pre_save.connect(pre_save_create_slug_for_cate, sender=VsCategory)

class VsSubCategoryes(models.Model):
    Category = models.ForeignKey(VsCategory,on_delete=models.CASCADE, null=True, blank=True,related_name="VsCategory_sub_cate")
    Title = models.CharField(max_length=120)
    Slug = models.CharField(max_length=120, null=True, blank=True)
    Status = models.BooleanField(default=True)
    Created_date = models.DateTimeField(default=django.utils.timezone.now)
    Created_By = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name="User_sub_cate")

    def __str__(self):
        return self.Title
    class Meta:
        verbose_name_plural = "VS Sub Categoryes"

def pre_save_create_slug_for_sub_cate(sender, instance, *args, **kwargs):
    if not instance.Slug:
        instance.Slug= slug_generator_for_sub_category(instance)

pre_save.connect(pre_save_create_slug_for_sub_cate, sender=VsSubCategoryes)



class VsReatingAttribute(models.Model):
    Title = models.CharField(max_length=120,unique=True)
    Slug = models.CharField(max_length=120, null=True, blank=True)
    Status = models.BooleanField(default=True)
    Description = models.TextField(null=True,blank=True)
    Reating_Range = models.IntegerField(default=0)
    Created_date = models.DateTimeField(default=django.utils.timezone.now)
    Created_By = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="User_VsReatingAttribute")

    def __str__(self):
        return self.Title
    class Meta:
        verbose_name_plural = "VS Reating Attribute"

def pre_save_create_slug_for_reat(sender, instance, *args, **kwargs):
    if not instance.Slug:
        instance.Slug= slug_generator_for_reating_review(instance)

pre_save.connect(pre_save_create_slug_for_reat, sender=VsReatingAttribute)


class VsConnectReatingWithCate(models.Model):
    Category = models.ForeignKey(VsCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="VsCategory_connect")
    Sub_Category = models.ForeignKey(VsSubCategoryes, on_delete=models.SET_NULL, null=True, blank=True, related_name="VsSubCategoryes_connect")
    Readint_attribute = models.ManyToManyField(VsReatingAttribute, blank=True, related_name="VsReatingAttribute_connect")
    Created_date = models.DateTimeField(default=django.utils.timezone.now)
    Created_By = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="User_VsConnectReatingWithCate")
    def __str__(self):
        return str(self.Category)
    class Meta:
        verbose_name_plural = "Vs Attribute Connet With Categoryes"

