# -*- coding: utf-8 -*-
from django.db import models
from account.models import VsUsers
from videos.models import VsVideos
import django
# Create your models here.

class VsFavourite(models.Model):
    Subscribe = models.ForeignKey(VsUsers, on_delete=models.SET_NULL, null=True, blank=True,related_name="VsUsers_VsFavourite")
    VsUser = models.ForeignKey(VsUsers, on_delete=models.SET_NULL, null=True, blank=True,related_name="User_VsFavourite")
    Video = models.ForeignKey(VsVideos, on_delete=models.SET_NULL, null=True, blank=True,related_name="VideoFavourite")
    Create_date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.VsUser)
    class Meta:
        verbose_name_plural = "VS Favourite"

class VsSendEmailForNewVideo(models.Model):
	Videos = models.ForeignKey(VsVideos, on_delete=models.SET_NULL, null=True, blank=True,related_name="VsVideos_SendEmailForNewVideo")
	VsUser = models.ForeignKey(VsUsers, on_delete=models.SET_NULL, null=True, blank=True,related_name="User_SendEmailForNewVideo")
	Send_date = models.DateTimeField(default=django.utils.timezone.now)

	def __str__(self):
		return str(self.Videos)
	class Meta:
		verbose_name_plural = "VS Send Email For New Video Upload."
