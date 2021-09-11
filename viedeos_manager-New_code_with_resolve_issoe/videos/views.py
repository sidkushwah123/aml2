from django.shortcuts import render,HttpResponseRedirect,HttpResponse,get_object_or_404,redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from .models import VsVideos,VsNonRegisterUser
from account.models import VsUsers
from django.views.decorators.csrf import csrf_exempt
import json
from categorys_and_reatings.models import VsCategory,VsSubCategoryes
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from datetime import date
from django.core.files.base import ContentFile
import base64
from project_control.models import VsSystemSettings
from django.db.models import F
from imratedme.utils import slug_generator_for_videos
from subscription.models import VsUserSubscriptionPayment
from imratedme import settings
# Create your views here.


def UpdateVideoVIdesView(request,video_id):
    get_video_objects = get_object_or_404(VsVideos,Videos_id=video_id)
    VsVideos.objects.filter(Videos_id=video_id).update(Views=F('Views')+1)
    response = HttpResponse("continue")
    system_settings = VsSystemSettings.objects.all().first()
    if request.user.username=="":
        if not request.COOKIES.get('user_id'):
            coocki_id = datetime.now()
            response.set_cookie('user_id', coocki_id)
        else:
            coocki_id  = request.COOKIES.get('user_id')
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')


        if system_settings.No_of_videos_watch_befure_login == 0:
            add_user = VsNonRegisterUser(user_id=coocki_id,Video=get_video_objects,User_ip=ip)
            add_user.save()
        else:
            get_user_watch_video_count = 0
            if VsNonRegisterUser.objects.filter(user_id=coocki_id).exists():
                get_user_watch_video_count = VsNonRegisterUser.objects.filter(user_id=coocki_id).count()
            if get_user_watch_video_count < system_settings.No_of_videos_watch_befure_login:
                add_user = VsNonRegisterUser(user_id=coocki_id,Video=get_video_objects,User_ip=ip)
                add_user.save()
            else:
                response = HttpResponse("break")
    else:
        response = HttpResponse("continue")
    return response


@csrf_exempt
def add_video_info(request):
    if request.method == "POST":
        video_id = request.POST['video_id']
        categorys = request.POST['categorys']
        sub_categorys = None
        if "sub_categorys" in request.POST:
            sub_categorys = request.POST['sub_categorys']
        video_name = request.POST['video_name']
        description = request.POST['description']

        meta_title = request.POST['video_name']
        if "meta_title" in request.POST:
            meta_title = request.POST['meta_title']

        meta_keyword = request.POST['meta_title']
        if "meta_keyword" in request.POST:
            meta_keyword = request.POST['meta_keyword']
        meta_description = ""
        if "meta_description" in request.POST:
            meta_description = request.POST['meta_description']
        get_videos_ins = get_object_or_404(VsVideos,Videos_id=video_id)
        get_videos_ins.Videos_Slug = slug_generator_for_videos(get_videos_ins)
        get_videos_ins.Videos_Title = video_name
        get_videos_ins.Categoryes_id = categorys
        get_videos_ins.Sub_Categoryes_id = sub_categorys
        get_videos_ins.Sub_Categoryes_id = sub_categorys
        get_videos_ins.Description = description
        get_videos_ins.Country = "test"
        get_videos_ins.Meta_Title = meta_title
        get_videos_ins.Meta_keyword = meta_keyword
        get_videos_ins.Meta_description = meta_description
        get_videos_ins.Publich_Status = True
        if request.POST["thumbnail"]:
            format, imgstr = request.POST["thumbnail"].split(';base64,')
            ext = format.split('/')[-1]
            dateTimeObj = datetime.now()
            today_date = date.today()
            set_file_name = str(today_date.day) + "_" + str(today_date.month) + "_" + str(today_date.year) + "_" + str(
                dateTimeObj.microsecond)
            file_name = set_file_name + "." + ext
            data = ContentFile(base64.b64decode(imgstr), name=file_name)
            get_videos_ins.Video_thumbnail.delete(save=False)
            get_videos_ins.Video_thumbnail = data
        get_videos_ins.save()
        return JsonResponse({"test": "data"})
    return HttpResponse("test")


@csrf_exempt
def get_sub_category(request):
    if request.method == "POST":
        get_cub_cate = None
        if VsSubCategoryes.objects.filter(Category_id = request.POST["get_cate_id"]).filter(Status=True).exists():
            get_cub_cate = VsSubCategoryes.objects.filter(Category_id = request.POST["get_cate_id"]).filter(Status=True).order_by("Title")
        return render(request,'web/videos/get_sub_category.html', {"get_cub_cate":get_cub_cate})
    return HttpResponse("Test")


@method_decorator(csrf_exempt , name="dispatch")
@method_decorator(login_required , name="dispatch")
class VideosAddView(generic.TemplateView):
    template_name = "web/videos/add_videos.html"


    def get(self, *args, **kwargs):
        Created_By = get_object_or_404(VsUsers, user=self.request.user)
        if not VsUserSubscriptionPayment.objects.filter(User=Created_By).filter(Active_status=True).exists():
            return redirect(settings.BASE_URL + "subscription/")
        return super().get(*args, **kwargs)


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            # return HttpResponseRedirect(reverse('admin_manage_setting:update_general',args=(get_data.id,)))
            return redirect(settings.BASE_URL+"admin/")
        else:
            return super(VideosAddView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = None
        if VsCategory.objects.filter(Status=True).exists():
            category = VsCategory.objects.filter(Status=True).order_by("Title")
        system_settings = VsSystemSettings.objects.all().first()
        set_upload_status = False
        Created_By = get_object_or_404(VsUsers, user=self.request.user)
        get_user_videos = VsVideos.objects.filter(Created_By=Created_By,Publich_Status=True).count()
        system_limit = 0
        error_message = ""
        if VsUserSubscriptionPayment.objects.filter(User=Created_By).filter(Active_status=True).exists():
            get_package_data = VsUserSubscriptionPayment.objects.filter(User=Created_By).filter(Active_status=True).last()
            if get_package_data.Expayer_date.date() >= datetime.today().date():
                system_limit = get_package_data.Upload_Video_limit
                error_message = "Your upload limit is end. You can upload only " + str(
                    system_limit) + " from one acount."
            else:
                system_limit = 0
                error_message = "Your membership is expired. please update your membership."
        else:
            system_limit = 0

        if get_user_videos >= system_limit:
            set_upload_status = True
        context['category'] = category
        context['upload_limit'] = system_limit
        context['my_uploaded_videos'] = get_user_videos
        context['set_upload_status'] = set_upload_status
        return context


    def post(self,request):
        status = "0"
        message = ""
        system_settings = VsSystemSettings.objects.all().first()
        Created_By = get_object_or_404(VsUsers, user=self.request.user)
        get_user_videos = VsVideos.objects.filter(Created_By=Created_By,Publich_Status=True).count()
        system_limit = 0
        error_message = ""
        if VsUserSubscriptionPayment.objects.filter(User=Created_By).filter(Active_status=True).exists():
            get_package_data = VsUserSubscriptionPayment.objects.filter(User=Created_By).filter(Active_status=True).last()
            if get_package_data.Expayer_date.date() >= datetime.today().date():
                system_limit = get_package_data.Upload_Video_limit
                error_message = "Your upload limit is end. You can upload only " + str(
                    system_limit) + " from one acount."
            else:
                system_limit = 0
                error_message = "Your membership is expired. please update your membership."
        else:
            system_limit = 0
        if get_user_videos >= system_settings.No_of_videos_uploaded_by_one_account:
            status = "1"
        if status == "1":
            message = "Your upload limit is end. You can upload only "+str(system_settings.No_of_videos_uploaded_by_one_account)+" from one acount."
        else:
            print("===================")
            Created_By = get_object_or_404(VsUsers ,  user=request.user)
            print(type(request.FILES['img_logo']))
            upload_file = request.FILES['img_logo']
            filename = "This is test video"
            get_objects = VsVideos(Video=upload_file,Created_By=Created_By)
            get_objects.save()
            print("===================")

        if self.request.is_ajax():
            return self.render_to_json_response({"status":status,"message":message, "video_id":get_objects.Videos_id,"videos":get_objects.Video.url}, status=200)
        else:
            return HttpResponseRedirect(reverse('videos:add_videos'))

    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)