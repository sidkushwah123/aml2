from .models import VsVideos
import django_filters

class VideosFilter(django_filters.FilterSet):
    class Meta:
        model = VsVideos
        fields = ['Videos_Title', ]