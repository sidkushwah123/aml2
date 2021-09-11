# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404,HttpResponse
from django.views import generic
from videos.models import VsRating
from manage_cms_page.models import VsCmsPage
from videos.models import VsVideos
from favourite_videos.models import VsFavourite,VsSendEmailForNewVideo
from account.models import VsUsers
from project_control.models import VsSystemSettings
from django.db.models import Count
from categorys_and_reatings.models import VsConnectReatingWithCate,VsCategory
from datetime import datetime, timedelta
from django.template.defaulttags import register
from django.template.loader import render_to_string
from django.db.models import Q,Subquery
from .models import VsHomePageSettings
from imratedme import settings
import email.message
import smtplib
# Create your views here.




@register.filter(name='get_total_video_count')
def get_total_video_count(category_objects):
	get_total_video_count = 0
	if VsVideos.objects.filter(Categoryes=category_objects).filter(Publich_Status=True).exists():
		get_total_video_count =  VsVideos.objects.filter(Categoryes=category_objects).filter(Publich_Status=True).count()
	return get_total_video_count


@register.filter(name='get_page_link_sidebar')
def get_page_link_sidebar(dummt_data):
    get_all_page = VsCmsPage.objects.all().order_by('set_order')
    return render_to_string('web/sidebar/page_link.html',{"get_all_page":get_all_page,'BASE_URL':settings.BASE_URL})

@register.filter(name='get_page_link')
def get_page_link(dummt_data):
    get_all_page = VsCmsPage.objects.all().order_by('set_order')
    return render_to_string('web/footer/page_link.html',{"get_all_page":get_all_page,'BASE_URL':settings.BASE_URL})


@register.filter(name='show_logo')
def show_logo(dummt_data):
	get_SystemSettings = VsSystemSettings.objects.all().order_by("id").first()
	return render_to_string('web/home/show_logo.html',{"get_SystemSettings":get_SystemSettings,"dummt_data":dummt_data})

@register.filter(name='show_project_title')
def show_project_title(dummt_data):
	get_SystemSettings = VsSystemSettings.objects.all().order_by("id").first()
	return get_SystemSettings.Project_Title

@register.filter(name='user_type')
def user_type(user):
	users_id = get_object_or_404(VsUsers,user=user)
	return users_id.Type


@register.filter(name='show_logo_and_title')
def show_logo_and_title(dummt_data):
	get_SystemSettings = VsSystemSettings.objects.all().order_by("id").first()
	return render_to_string('web/home/show_logo_and_favicon.html',{"get_SystemSettings":get_SystemSettings,"dummt_data":dummt_data})

@register.filter(name='get_social_link')
def get_social_link(dummt_data):
	get_data_of_home_page = VsHomePageSettings.objects.all().order_by("id").first()
	return render_to_string('web/home/social_link.html',{"get_data_of_home_page":get_data_of_home_page,"dummt_data":dummt_data})

@register.filter(name='get_category_data')
def get_category_data(category_id):
	category_data =get_object_or_404(VsCategory,id=category_id['Categoryes'])
	return render_to_string('web/home/get_category_data.html',{"category_id":category_id,"category_data":category_data})



@register.filter(name='get_reating_data')
def get_reating_data(video_objects):
	if VsConnectReatingWithCate.objects.filter(Category=video_objects.Categoryes).filter(Sub_Category=video_objects.Sub_Categoryes).exists():
		get_reating =  get_object_or_404(VsConnectReatingWithCate,Category=video_objects.Categoryes,Sub_Category=video_objects.Sub_Categoryes)
	content = {}
	content["get_reating"] = get_reating
	content["video"] = video_objects
	return render_to_string('web/home/reating.html',content)

@register.filter(name='get_last_uploaded_vido_by')
def get_last_uploaded_vido_by(dummt_data):
	get_videp = VsVideos.objects.filter(Publich_Status=True).order_by("-id").first()
	content = {}
	content["video_info"] = get_videp
	return render_to_string('web/home/show_user_info.html',content)

@register.filter(name='get_last_uploaded_vido_on')
def get_last_uploaded_vido_on(dummt_data):
	get_videp = VsVideos.objects.filter(Publich_Status=True).order_by("-id").first()
	return get_videp.Created_date

class HomeView(generic.TemplateView):
    template_name = "web/home/home.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        videos_of_tha_day = None
        get_data_of_home_page = VsHomePageSettings.objects.all().order_by("id").first()
        # if VsVideos.objects.filter(Publich_Status=True).exists():
        # 	videos_of_tha_day =  VsVideos.objects.filter(Publich_Status=True).order_by("-Updated_date").first()
        # context["videos_of_tha_day"] = videos_of_tha_day
        context["get_data_of_home_page"] = get_data_of_home_page
        # ==================================================================================
        get_reating= None
        if VsConnectReatingWithCate.objects.filter(Category=get_data_of_home_page.Video_Of_The_Day.Categoryes).filter(Sub_Category=get_data_of_home_page.Video_Of_The_Day.Sub_Categoryes).exists():
            get_reating =  get_object_or_404(VsConnectReatingWithCate,Category=get_data_of_home_page.Video_Of_The_Day.Categoryes,Sub_Category=get_data_of_home_page.Video_Of_The_Day.Sub_Categoryes)
        context["get_reating"] = get_reating
        count_users= VsUsers.objects.all().count()
        context["count_users"] = count_users
        # ====================================================================================
        voters = None
        if VsRating.objects.values('User').annotate(dcount=Count('User')).exists():
        	 res_ = VsRating.objects.values('User').annotate(dcount=Count('User'))
        	 voters = len(res_)
        context["voters"] = voters
        # ====================================================================================
        total_video = 0
        if VsVideos.objects.filter(Publich_Status=True).exists():
        	total_video = VsVideos.objects.filter(Publich_Status=True).count()
        context["total_video"] = total_video
        # ===================================================================================
        # ====================================================================================
        get_letest_video = None
        if VsVideos.objects.filter(Publich_Status=True).exists():
        	get_letest_video = VsVideos.objects.filter(Publich_Status=True).order_by("-id")[0:3]
        context["get_letest_video"] = get_letest_video
        # ==========================================================================================
        get_top_reated = None
        get_top_categoryes = None
        if VsVideos.objects.filter(Publich_Status=True).exists():
        	get_top_reated = VsVideos.objects.filter(Publich_Status=True).order_by("-Reating")[0:3]
        	get_top_categoryes_id = VsVideos.objects.values('Categoryes').annotate(dcount=Count('Categoryes')).order_by('-dcount')[0:3]
        	# print("=====================")
        	# print(get_top_categoryes_id)
        	# print("========================")
        	# get_top_categoryes = VsCategory.objects.filter(id__in=Subquery(get_top_categoryes_id.values("Categoryes")))
        context["get_top_reated"] = get_top_reated
        context["get_top_categoryes"] = get_top_categoryes_id
        return context


class PageContentView(generic.TemplateView):
	template_name = "web/home/cms_pagge.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		page_content = None
		keyword = self.kwargs.get("keyword")
		if VsCmsPage.objects.filter(keyword=keyword).exists():
			page_content =VsCmsPage.objects.filter(keyword=keyword).first()
		context['page_content'] = page_content
		return context


def SendMailVIew(request):
	get_system_info = VsSystemSettings.objects.all().first()
	get_video_data = VsVideos.objects.filter(mail_send_status=False).filter(Publich_Status=True).order_by("-id")
	# data_content = {"get_system_info": get_system_info,"BASE_URL": settings.BASE_URL,"get_video_info":get_video_info}
	# email_content = render_to_string("email_template/video_notification_on_email.html", data_content)
	# msg = email.message.Message()
	# msg['Subject'] = str(get_video_info.Created_By)+' just uploaded a video'
	# msg['From'] = settings.EMAIL_HOST_USER
	# # msg['To'] = user.VsUser.user.email
	# msg['To'] = "notageeks@gmail.com"
	# password = settings.EMAIL_HOST_PASSWORD
	# msg.add_header('Content-Type', 'text/html')
	# msg.set_payload(email_content)
	# s = smtplib.SMTP(settings.EMAIL_HOST + ':' + str(settings.EMAIL_PORT))
	# s.starttls()
	# s.login(msg['From'], password)
	# s.sendmail(msg['From'], [msg['To']], msg.as_string())
	# print("send")
	# print("-----------------")
	for get_video_info in get_video_data:
		data_content = {"get_system_info": get_system_info,"BASE_URL": settings.BASE_URL,"get_video_info":get_video_info}
		email_content = render_to_string("email_template/video_notification_on_email.html", data_content)
		if VsFavourite.objects.filter(Subscribe=get_video_info.Created_By).exists():
			get_users = VsFavourite.objects.filter(Subscribe=get_video_info.Created_By)
			for user in get_users:
				if VsSendEmailForNewVideo.objects.filter(Videos=get_video_info).filter(VsUser=user.VsUser).exists():
					test = "test"
				else:
					msg = email.message.Message()
					msg['Subject'] = str(get_video_info.Created_By)+' just uploaded a video'
					msg['From'] = settings.EMAIL_HOST_USER
					msg['To'] = str(user.VsUser.user.email)
					password = settings.EMAIL_HOST_PASSWORD
					msg.add_header('Content-Type', 'text/html')
					msg.set_payload(email_content)
					s = smtplib.SMTP(settings.EMAIL_HOST + ':' + str(settings.EMAIL_PORT))
					s.starttls()
					s.login(msg['From'], password)
					s.sendmail(msg['From'], [msg['To']], msg.as_string())
					add_mail_stats = VsSendEmailForNewVideo(Videos=get_video_info,VsUser=user.VsUser)
					add_mail_stats.save()
					VsVideos.objects.filter(Videos_id=get_video_info.Videos_id).update(mail_send_status=True)
	return HttpResponse("test")