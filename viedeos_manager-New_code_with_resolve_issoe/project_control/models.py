from django.db import models
from datetime import date
import django
# Create your models here.


def user_directory_path(instance, filename):
    today_date = date.today()
    return '{0}/{1}'.format("system_settings/logo/"+str(today_date.year)+"/"+str(today_date.month)+"/"+str(today_date.day),filename)

def user_directory_path_favicon(instance, filename):
    today_date = date.today()
    return '{0}/{1}'.format("system_settings/favicon/"+str(today_date.year)+"/"+str(today_date.month)+"/"+str(today_date.day),filename)

class VsSystemSettings(models.Model):
    Project_Title = models.CharField(max_length=120)
    Tag_Line = models.CharField(max_length=120,null=True,blank=True)
    Logo = models.ImageField(upload_to=user_directory_path)
    Favicon_Icon = models.ImageField(upload_to=user_directory_path_favicon)
    No_of_videos_watch_befure_login = models.IntegerField(default=0 , help_text="0 miens unlimited")
    No_of_videos_watch_after_login = models.IntegerField(default=0 , help_text="0 miens unlimited")
    No_of_videos_uploaded_by_one_account = models.IntegerField(default=0 , help_text="0 miens unlimited")
    Promotional_Email = models.EmailField(null=True,blank=True)
    Promotional_Email_password = models.CharField(max_length=120, null=True,blank=True)
    Created_date = models.DateTimeField(default=django.utils.timezone.now)
    Updated_date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.Project_Title
    class Meta:
        verbose_name_plural = "VS System Settings"


