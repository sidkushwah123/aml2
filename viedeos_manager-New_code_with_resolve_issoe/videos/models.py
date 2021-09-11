# -*- coding: utf-8 -*-
from django.db import models
from datetime import date
import django
from account.models import VsUsers
from categorys_and_reatings.models import  VsCategory,VsSubCategoryes,VsReatingAttribute
from django.db.models.signals import pre_save
from imratedme.utils import slug_generator_for_videos,unique_id_generator
# Create your models here.

def user_directory_path(instance, filename):
    producer_id_in_list = instance.Created_By.name.split(" ")
    today_date = date.today()
    producer_id_in_string = '_'.join([str(elem) for elem in producer_id_in_list])
    return '{0}/{1}'.format('videos/'+producer_id_in_string+"/"+str(today_date.year)+"/"+str(today_date.month)+"/"+str(today_date.day),filename)
def user_directory_path_thumbnail(instance, filename):
    producer_id_in_list = instance.Created_By.name.split(" ")
    today_date = date.today()
    producer_id_in_string = '_'.join([str(elem) for elem in producer_id_in_list])
    return '{0}/{1}'.format("videos/"+producer_id_in_string+"/"+str(today_date.year)+"/"+str(today_date.month)+"/"+str(today_date.day)+"/thumbnail",filename)

class VsVideos(models.Model):
    Videos_Title = models.CharField(max_length=500)
    Videos_id = models.CharField(max_length=500)
    Videos_Slug = models.CharField(max_length=500,null=True,blank=True)
    Categoryes = models.ForeignKey(VsCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="VsCategory_VsVideos")
    Sub_Categoryes = models.ForeignKey(VsSubCategoryes, on_delete=models.SET_NULL, null=True, blank=True, related_name="VsSubCategoryes_VsVideos")
    Video = models.FileField(null=True,upload_to=user_directory_path)
    Video_thumbnail = models.ImageField(null=True,upload_to=user_directory_path_thumbnail,blank=True)
    Publich_Status = models.BooleanField(default=False)
    Country = models.CharField(max_length=120,null=True,blank=True)
    Description = models.TextField(null=True,blank=True)
    Meta_Title = models.CharField(max_length=200,null=True,blank=True)
    Meta_keyword = models.CharField(max_length=120,null=True,blank=True)
    Meta_description = models.TextField(null=True,blank=True)
    Created_date = models.DateTimeField(default=django.utils.timezone.now)
    Views = models.IntegerField(default=0)
    Reating = models.IntegerField(default=0)
    Updated_date = models.DateTimeField(default=django.utils.timezone.now)
    mail_send_status  = models.BooleanField(default=False)
    Created_By = models.ForeignKey(VsUsers, on_delete=models.SET_NULL, null=True, blank=True, related_name="User_VsVideos")

    def __str__(self):
        return self.Videos_Title
    class Meta:
        verbose_name_plural = "VS Videos"

    def save(self, *args, **kwargs):
        value = self.Videos_Title
        self.Videos_Slug = slug_generator_for_videos(self)
        super().save(*args, **kwargs)


def pre_save_create_slug_for_videos(sender, instance, *args, **kwargs):
    if not instance.Videos_Slug:
        instance.Videos_Slug= slug_generator_for_videos(instance)

pre_save.connect(pre_save_create_slug_for_videos, sender=VsVideos)

def pre_save_create_video_id(sender, instance, *args, **kwargs):
    if not instance.Videos_id:
        instance.Videos_id= unique_id_generator(instance)
pre_save.connect(pre_save_create_video_id, sender=VsVideos)



class VsComments(models.Model):
    Video = models.ForeignKey(VsVideos, on_delete=models.CASCADE, null=True, blank=True, related_name="User_VsComments")
    User = models.ForeignKey(VsUsers, on_delete=models.CASCADE, null=True, blank=True, related_name="User_VsComments")
    Comment = models.TextField()
    Status = models.BooleanField(default=True)
    Created_date = models.DateTimeField(default=django.utils.timezone.now)
    Updated_date= models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.User)

    class Meta:
        verbose_name_plural = "VS Comments"

class VsRating(models.Model):
    Video = models.ForeignKey(VsVideos, on_delete=models.CASCADE, null=True, blank=True, related_name="VsVideos_VsReating")
    User = models.ForeignKey(VsUsers, on_delete=models.CASCADE, null=True, blank=True, related_name="VsUsers_VsReating")
    Reating_attrbute = models.ForeignKey(VsReatingAttribute, on_delete=models.CASCADE, null=True, blank=True, related_name="User_VsReatingAttribute")
    Reating = models.IntegerField(default=0)
    Status = models.BooleanField(default=True)
    Created_date = models.DateTimeField(default=django.utils.timezone.now)
    Updated_date = models.DateTimeField(default=django.utils.timezone.now)


    def __str__(self):
        return str(self.User)

    class Meta:
        verbose_name_plural = "VS Rating"


class VsNonRegisterUser(models.Model):
    user_id = models.CharField(max_length=500,null=True)
    Video = models.ForeignKey(VsVideos, on_delete=models.CASCADE, null=True, blank=True, related_name="VsVideos_VsNonRegisterUser")
    watch_date = models.DateTimeField(default=django.utils.timezone.now)
    User_ip = models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name_plural = "VS Non Register User"