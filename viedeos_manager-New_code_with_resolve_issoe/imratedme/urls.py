"""imratedme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', include('django.contrib.auth.urls')),
    path('', include(('home.urls','home'),namespace='home')),
    path('account/', include(('account.urls','account'),namespace='account')),
    path('video/', include(('videos.urls','videos'),namespace='videos')),
    path('profiles/', include(('profiles.urls','profiles'),namespace='profiles')),
    path('dashboard/', include(('my_videos.urls','my_videos'),namespace='my_videos')),
    path('videos-detail/', include(('videos_detail.urls','videos_detail'),namespace='videos_detail')),
    path('favourite-videos/', include(('favourite_videos.urls','favourite_videos'),namespace='favourite_videos')),
    path('search/', include(('search.urls','search'),namespace='search')),
    path('subscription/', include(('subscription.urls','subscription'),namespace='subscription')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)