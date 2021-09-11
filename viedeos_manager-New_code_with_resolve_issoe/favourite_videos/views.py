from django.shortcuts import render,HttpResponse,get_object_or_404
from account.models import VsUsers
from videos.models import VsVideos
from .models import VsFavourite
from django.http import HttpResponse, JsonResponse
# Create your views here.


def Checkfavourite_videos_list(request,video_id):
    if video_id:
        get_video_ins  = get_object_or_404(VsVideos,Videos_id=video_id)
        get_user_ins = get_object_or_404(VsUsers,user=request.user)
        if VsFavourite.objects.filter(Subscribe=get_video_ins.Created_By).filter(VsUser=get_user_ins).exists():
            status = "1"
        else:
            status = "0"
    return JsonResponse({"status":status})

def updatefavourite_videos_list(request,video_id):
    if video_id:
        status = "0"
        message = ""
        get_video_ins  = get_object_or_404(VsVideos,Videos_id=video_id)
        get_user_ins = get_object_or_404(VsUsers,user=request.user)
        if VsFavourite.objects.filter(Subscribe=get_video_ins.Created_By).filter(VsUser=get_user_ins).exists():
            VsFavourite.objects.filter(Subscribe=get_video_ins.Created_By).filter(VsUser=get_user_ins).delete()
            status = "1"
            message = "Video remove in your favourite list."
        else:
            add_data = VsFavourite(Subscribe=get_video_ins.Created_By,VsUser=get_user_ins,Video=get_video_ins)
            add_data.save()
            status = "0"
            message = "Video add in your favourite list."
    return JsonResponse({"status":status,"message":message})