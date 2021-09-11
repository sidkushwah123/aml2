from django.db import models
from datetime import date
# Create your models here.


def user_directory_path_backgrount_image(instance, filename):
    producer_id_in_list = instance.keyword.split(" ")
    today_date = date.today()
    producer_id_in_string = '_'.join([str(elem) for elem in producer_id_in_list])
    return '{0}/{1}'.format("cms/background/"+producer_id_in_string+"/"+str(today_date.year)+"/"+str(today_date.month)+"/"+str(today_date.day)+"/thumbnail",filename)


class VsCmsPage(models.Model):
    Title  = models.CharField(max_length=500,unique=True)
    keyword = models.CharField(max_length=500,unique=True)
    Background_Image = models.ImageField(null=True,upload_to=user_directory_path_backgrount_image,blank=True)
    Description = models.TextField(null=True,blank=True)
    Page_content = models.TextField(null=True,blank=True)
    set_order = models.IntegerField(default=0)
    def __str__(self):
       return self.Title
    class Meta:
    	verbose_name_plural = "VS CMS Page Content"