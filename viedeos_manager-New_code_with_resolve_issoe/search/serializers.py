from videos.models import VsVideos
from rest_framework import serializers



class GetVideoSerializers(serializers.ModelSerializer):
    class Meta:
        model = VsVideos
        fields = ['id', 'Videos_Title', 'Videos_id', 'Videos_Slug', 'Categoryes', 'Sub_Categoryes',
                  'Country', 'Description', 'Meta_Title', 'Meta_keyword','Meta_description','Created_date','Views','Updated_date','Created_By']
        depth = 2