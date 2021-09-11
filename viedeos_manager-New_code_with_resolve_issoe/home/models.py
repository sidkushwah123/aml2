from django.db import models
from videos.models import VsVideos
from datetime import date
import django
# Create your models here.


def user_directory_path_thumbnail(instance, filename):
    producer_id_in_list = instance.Video_Of_The_Day.Videos_Title.split(" ")
    today_date = date.today()
    producer_id_in_string = '_'.join([str(elem) for elem in producer_id_in_list])
    return '{0}/{1}'.format("home_page_setting/"+producer_id_in_string+"/"+str(today_date.year)+"/"+str(today_date.month)+"/"+str(today_date.day)+"/thumbnail",filename)

def user_directory_path_sessing_image(instance, filename):
    producer_id_in_list = instance.Session_2_Title.split(" ")
    today_date = date.today()
    producer_id_in_string = '_'.join([str(elem) for elem in producer_id_in_list])
    return '{0}/{1}'.format("Session_2/"+producer_id_in_string+"/"+str(today_date.year)+"/"+str(today_date.month)+"/"+str(today_date.day)+"/thumbnail",filename)

def user_directory_path_Session_3_box_1_Image(instance, filename):
    producer_id_in_list = instance.Session_3_box_1_Title.split(" ")
    today_date = date.today()
    producer_id_in_string = '_'.join([str(elem) for elem in producer_id_in_list])
    return '{0}/{1}'.format("Session_2_box_1/"+producer_id_in_string+"/"+str(today_date.year)+"/"+str(today_date.month)+"/"+str(today_date.day)+"/thumbnail",filename)

def user_directory_path_Session_3_box_2_Image(instance, filename):
    producer_id_in_list = instance.Session_3_box_2_Title.split(" ")
    today_date = date.today()
    producer_id_in_string = '_'.join([str(elem) for elem in producer_id_in_list])
    return '{0}/{1}'.format("Session_2_box_2/"+producer_id_in_string+"/"+str(today_date.year)+"/"+str(today_date.month)+"/"+str(today_date.day)+"/thumbnail",filename)

def user_directory_path_Session_3_box_3_Image(instance, filename):
    producer_id_in_list = instance.Session_3_box_3_Title.split(" ")
    today_date = date.today()
    producer_id_in_string = '_'.join([str(elem) for elem in producer_id_in_list])
    return '{0}/{1}'.format("Session_2_box_3/"+producer_id_in_string+"/"+str(today_date.year)+"/"+str(today_date.month)+"/"+str(today_date.day)+"/thumbnail",filename)

class VsHomePageSettings(models.Model):
	Video_Of_The_Day = models.ForeignKey(VsVideos, on_delete=models.SET_NULL, null=True, blank=True,related_name="Video_Of_The_Day_HomePageSettings")
	Video_Of_The_Day_Thumbnail = models.ImageField(null=True,upload_to=user_directory_path_thumbnail,blank=True)
	Session_2_Title = models.CharField(max_length=500)
	Session_2_description = models.TextField()
	Session_2_Image = models.ImageField(null=True,upload_to=user_directory_path_sessing_image,blank=True)
	Session_3_box_1_Title = models.CharField(max_length=500)
	Session_3_box_1_description = models.TextField()
	Session_3_box_1_Image = models.ImageField(null=True,upload_to=user_directory_path_Session_3_box_1_Image,blank=True)
	Session_3_box_1_Counter_start = models.IntegerField(default=0)
	Session_3_box_2_Title = models.CharField(max_length=500)
	Session_3_box_2_description = models.TextField()
	Session_3_box_2_Image = models.ImageField(null=True,upload_to=user_directory_path_Session_3_box_2_Image,blank=True)
	Session_3_box_2_Counter_start = models.IntegerField(default=0)
	Session_3_box_3_Title = models.CharField(max_length=500)
	Session_3_box_3_description = models.TextField()
	Session_3_box_3_Image = models.ImageField(null=True,upload_to=user_directory_path_Session_3_box_3_Image,blank=True)
	Session_3_box_3_Counter_start = models.IntegerField(default=0)
	Videos_Of_The_Week = models.ManyToManyField(VsVideos, blank=True, related_name="Videos_Of_The_Week_HomePageSettings")
	Facebook_Page_Link = models.URLField(null=True,blank=True)
	LinkedIn_Page_Link = models.URLField(null=True,blank=True)
	Twitter_Page_Link = models.URLField(null=True,blank=True)
	Instagram_Page_Link = models.URLField(null=True,blank=True)
	Updated_date = models.DateTimeField(default=django.utils.timezone.now)

	def __str__(self):
		return str(self.Video_Of_The_Day)
	class Meta:
		verbose_name_plural = "VS Home Page Settings"