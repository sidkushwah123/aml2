from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from django.views import generic
from videos.models import VsVideos,VsComments,VsRating,VsComments
from account.models import VsUsers
from django.http import  JsonResponse
from django.template.defaulttags import register
from django.utils.decorators import method_decorator
from django.db.models import Count,Sum,Avg,F
from categorys_and_reatings.models import VsConnectReatingWithCate,VsReatingAttribute
from django.views.generic.base import TemplateView
from django.template.loader import render_to_string
from project_control.models import VsSystemSettings
from imratedme import settings
# Create your views here.




def UpdateVideoVIdesView(request,video_id):
    return HttpResponse("skjfnj")

@register.simple_tag
def get_overall_of_attribute(attribute,video):
    all_reating = []
    all_total = []
    if VsRating.objects.filter(Video=video).filter(Reating_attrbute=attribute).filter(Status=True).exists():
        get_all_rating_data = VsRating.objects.filter(Video=video).filter(Reating_attrbute=attribute).filter(Status=True)
        for item in get_all_rating_data:
            all_reating.append(item.Reating)
            all_total.append(item.Reating_attrbute.Reating_Range)
    sum_of_reating = sum(all_reating)
    sum_of_total = sum(all_total)
    if sum_of_total == 0:
        average = 0
    else:
        precentage = (sum_of_reating * 100) / sum_of_total
        average = precentage / 10
    return int(average * 10)


@register.filter(name='ger_user_image')
def ger_user_image(user):
    get_image = None
    if VsUsers.objects.filter(user=user).exists():
        get_image  = get_object_or_404(VsUsers,user=user)
        if get_image.Image:
            return get_image.Image.url
        else:
            if VsSystemSettings.objects.all().order_by("id").exists():
                get_SystemSettings = VsSystemSettings.objects.all().order_by("id").first()
                if get_SystemSettings.Logo:
                    return get_SystemSettings.Logo.url
                else:
                    return "/static/web/dummyUser.jpg"
            else:
                return "/static/web/dummyUser.jpg"
    else:
        return "/static/web/dummyUser.jpg"

@register.simple_tag
def get_rating(user_ins,video_ins,attri_ins,inc_time=1):
    reating = 0
    if VsUsers.objects.filter(user=user).exists():
        vs_user = get_object_or_404(VsUsers,user=user_ins)
        if VsRating.objects.filter(Video=video_ins).filter(User=vs_user).filter(Reating_attrbute=attri_ins).exists():
            get_data = get_object_or_404(VsRating,Video=video_ins,User=vs_user,Reating_attrbute=attri_ins)
            reating = get_data.Reating
        return reating*int(inc_time)
    else:
        return reating

@register.simple_tag
def get_comment(user_ins,video_ins):
    comment = ""
    vs_user = get_object_or_404(VsUsers,user=user_ins)
    if VsComments.objects.filter(Video=video_ins).filter(User=vs_user).exists():
        get_data = get_object_or_404(VsComments,Video=video_ins,User=vs_user)
        comment = get_data.Comment
    return comment



@register.filter(name='get_value_in_ten_time')
def get_value_in_ten_time(value):
    return float(value)*10

@register.simple_tag
def get_votes_data(user_id,video):
    get_vs_user_data = None
    get_reating = None
    get_coment = None
    if VsUsers.objects.filter(id=user_id['User']).exists():
        get_vs_user_data = get_object_or_404(VsUsers,id=user_id['User'])
    
        if VsRating.objects.filter(User=get_vs_user_data).filter(Video=video).exists():
            get_reating = VsRating.objects.filter(User=get_vs_user_data).filter(Video=video)
        if VsComments.objects.filter(User=get_vs_user_data).filter(Video=video).exists():
            get_coment = get_object_or_404(VsComments,User=get_vs_user_data,Video=video)
    user_data = {"get_vs_user_data":get_vs_user_data,"get_reating":get_reating,"get_coment":get_coment}
    return render_to_string("web/videos_detail/voters_info.html",user_data)

@register.simple_tag
def get_one_video_overview_of_overview(video):
    all_reating = [0]
    all_total = []
    if VsRating.objects.filter(Video=video).filter(Status=True).exists():
        all_total = VsRating.objects.values('User').filter(Video=video).filter(Status=True).annotate(total=Count('id'))
        for item in all_total:
            if VsUsers.objects.filter(id=item['User']).exists():
                get_user = get_object_or_404(VsUsers,id=item['User'])
                test_data = get_user
                all_reating.append(get_one_user_overview(get_user, video))
    total = sum(all_reating)
    total_user = len(all_total)
    # return int(average*10)
    return int(total/total_user)


@register.simple_tag
def get_one_user_overview(user_id,video):
    all_reating = []
    all_total = []

    if VsRating.objects.filter(Video=video).filter(User=user_id).filter(Status=True).exists():
        get_all_rating_data = VsRating.objects.filter(Video=video).filter(User=user_id).filter(Status=True)
        for item in get_all_rating_data:
            all_reating.append(item.Reating)
            all_total.append(item.Reating_attrbute.Reating_Range)
    sum_of_reating = sum(all_reating)
    sum_of_total = sum(all_total)
    if sum_of_total == 0:
        average = 0
    else:
        precentage = (sum_of_reating*100)/sum_of_total
        average = precentage/10
    return int(average*10)


@register.filter(name='get_average_of_reating')
def get_average_of_reating(video_ins):
    get_data  = video_ins
    all_reating = []
    all_total = []
    if VsRating.objects.filter(Video=get_data).filter(Status=True).exists():
        get_all_rating_data = VsRating.objects.filter(Video=get_data).filter(Status=True)
        for item in get_all_rating_data:
            all_reating.append(item.Reating)
            all_total.append(item.Reating_attrbute.Reating_Range)
    sum_of_reating = sum(all_reating)
    sum_of_total= sum(all_total)
    if sum_of_total == 0:
        average = 0
    else:    
        precentage = (sum_of_reating*100)/sum_of_total
        average = precentage/10
    return round(average,1)




class VideosDetailView(generic.DetailView):
    template_name = "web/videos_detail/details.html"
    queryset = VsVideos.objects.all()

    def get_object(self):
        get_data =  None
        if VsVideos.objects.filter(Videos_id=self.kwargs.get("video_id")).exists():
            get_data = get_object_or_404(VsVideos, Videos_id=self.kwargs.get("video_id"))
        return get_data

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            # return HttpResponseRedirect(reverse('admin_manage_setting:update_general',args=(get_data.id,)))
            return redirect(settings.BASE_URL+"admin/")
        else:
            return super(VideosDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_info = None
        get_user = None
        if VsVideos.objects.filter(Videos_id=self.kwargs.get("video_id")).exists():
            get_data = get_object_or_404(VsVideos, Videos_id=self.kwargs.get("video_id"))
            get_user = get_data.Created_By
        get_all_videos = None
        get_reating= None
        if VsConnectReatingWithCate.objects.filter(Category=get_data.Categoryes).filter(Sub_Category=get_data.Sub_Categoryes).exists():
            get_reating =  get_object_or_404(VsConnectReatingWithCate,Category=get_data.Categoryes,Sub_Category=get_data.Sub_Categoryes)
        context["get_reating"] = get_reating
        if VsVideos.objects.filter(Created_By=get_user).filter(Publich_Status=True).exists():
            get_all_videos = VsVideos.objects.filter(Created_By=get_user).filter(Publich_Status=True)
        context["get_all_video"] = get_all_videos

        # ====================get review Info===========================
        get_review = VsRating.objects.values('User').filter(Video=get_data).filter(Status=True).annotate(total=Count('id'))

        # get_reating_no =  VsRating.objects.filter(Video=get_data).filter(Status=True).aggregate(Sum('Reating'))
        # ----------------------------------------------------------
        get_data  = get_data
        all_reating = []
        all_total = []
        if VsRating.objects.filter(Video=get_data).filter(Status=True).exists():
            get_all_rating_data = VsRating.objects.filter(Video=get_data).filter(Status=True)
            for item in get_all_rating_data:
                all_reating.append(item.Reating)
                all_total.append(item.Reating_attrbute.Reating_Range)
        sum_of_reating = sum(all_reating)
        sum_of_total= sum(all_total)
        if sum_of_total == 0:
            average = 0
        else:    
            precentage = (sum_of_reating*100)/sum_of_total
            average = precentage/10
        # ----------------------------------------------------------
        VsVideos.objects.filter(Videos_id=self.kwargs.get("video_id")).update(Reating=average)
        context["total_botes"] = len(get_review)
        context["botes"] = get_review
        
        context["total_rating"] = sum_of_reating
        # ========================================================================
        print("================")
        print(context)
        print("================")
        return context


    def post(self, request, *args, **kwargs):  
        get_video_ins  = get_object_or_404(VsVideos,Videos_id=request.POST["videos_id"])
        user_ins = get_object_or_404(VsUsers, user=request.user)
        message_set = ""
        message = ""
        for item in request.POST.getlist('range_name'):
            print("===========") 
            print(item) 
            print(request.POST["range_"+item]) 
            get_rating_ins = get_object_or_404(VsReatingAttribute,id=item)
            if VsRating.objects.filter(Video=get_video_ins).filter(User=user_ins).filter(Reating_attrbute=get_rating_ins).exists():
                # VsRating.objects.filter(Video=get_video_ins).filter(User=user_ins).filter(Reating_attrbute=get_rating_ins).update(Reating=request.POST["range_"+item])
                message = "On this video you are already given rated"

            else:
                add_rating  =  VsRating(Video=get_video_ins,User=user_ins,Reating_attrbute=get_rating_ins,Reating=request.POST["range_"+item]) 
                add_rating.save()
                message = "Your rating is added successfully. Thank You for your valuable rating"
        message_2 = ""
        if request.POST["comments"] != "":
            message_2 = " & Comment"
            if VsComments.objects.filter(Video=get_video_ins).filter(User=user_ins).exists():
                terst = ""
                # VsComments.objects.filter(Video=get_video_ins).filter(User=user_ins).update(Comment=request.POST["comments"])
            else:
                add_comment = VsComments(Video=get_video_ins,User=user_ins,Comment=request.POST["comments"])
                add_comment.save()
        if message == "":
            message_set = "Comment add successfully."
        else:
            message_set  =  message+message_2+"."
        return JsonResponse({"message":message_set})
