from django.shortcuts import render,get_object_or_404,HttpResponseRedirect,HttpResponse,redirect
from django.views import generic
from .forms import SignUpForm,VsUsersForm
from django.contrib import messages
import string
from django.urls import reverse
import random
import email.message
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from imratedme import settings
import smtplib
from .models import VsUsers
from datetime import datetime
from datetime import date
from django.urls import reverse_lazy
from project_control.models import VsSystemSettings
from subscription.models import VsUserSubscriptionPayment,VsSubscription
from django import forms
# Create your views here.

def test_mail(request):
    email_content = "<h1>Deepak</h1>"
    msg = email.message.Message()
    msg['Subject'] = 'XXXX is your OTP to verify and complete registration with iamRatedme.com'
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = 'applicationsupport@imratedme.com'
    password = settings.EMAIL_HOST_PASSWORD
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(email_content)
    s = smtplib.SMTP(settings.EMAIL_HOST + ':' + str(settings.EMAIL_PORT))
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    ################################################ EMAL SEND CODE END ##############
    messages.info(request, 'New varification code is sed to your email id.')
    return  HttpResponse("test")

def Send_opt(request,user_id):
    if VsUsers.objects.filter(id=user_id).exists():
        get_data = get_object_or_404(VsUsers, id=user_id)
        if get_data.user.is_active:
            messages.error(request, 'Your account is already varified.')
        else:
            otp = ''.join([random.choice(string.digits) for i in range(0, 4)])
            VsUsers.objects.filter(id=user_id).update(otp=otp)
            ################################################ EMAL SEND CODE START ##############
            get_system_info = VsSystemSettings.objects.all().first()
            data_content = {"yourname": get_data.name, "user_email": get_data.user.email, "otp": otp,
                            "get_system_info": get_system_info}
            email_content = render_to_string('email_template/email_send_for_create_new_account.html', data_content)
            msg = email.message.Message()
            msg['Subject'] = str(otp)+' is your OTP to verify and complete registration with iamRatedme.com'
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = get_data.user.email
            password = settings.EMAIL_HOST_PASSWORD
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(email_content)
            s = smtplib.SMTP(settings.EMAIL_HOST + ':' + str(settings.EMAIL_PORT))
            s.starttls()
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string())
            ################################################ EMAL SEND CODE END ##############
            messages.info(request, 'New varification code is sed to your email id.')
    else:
        messages.error(request, 'Your user_id is incorrect.')
    return HttpResponse("test")


class VarificationView(generic.TemplateView):
    template_name = "web/account/varification.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_code = self.kwargs.get("user_code")
        get_data  = None
        if VsUsers.objects.filter(user_code=user_code).exists():
            get_data = get_object_or_404(VsUsers , user_code=user_code)
        context["user_info"] = get_data
        return context

    def post(self,request,user_code=""):
        user_id = request.POST["user_id"]
        otp_code = request.POST["code_1"]+request.POST["code_2"]+request.POST["code_3"]+request.POST["code_4"]

        otp = ''.join([random.choice(string.digits) for i in range(0, 4)])
        print(otp_code)
        if VsUsers.objects.filter(id=user_id).exists():
            get_data = get_object_or_404(VsUsers ,id=user_id)
            otp = ''.join([random.choice(string.digits) for i in range(0, 4)])
            get_varify_status = get_object_or_404(User,id=get_data.user.id)
            if get_varify_status.is_active:
                messages.info(request, 'Account Already Varify Successfully.')
                password = get_data.password
                username = get_data.user.username
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    if user.is_superuser:
                        messages.error(request, "This login area is not used for superadmin.")
                    else:
                        if user.is_active:
                            login(request, user)
                            return redirect(settings.BASE_URL + "account/dashboard")
                        else:
                            messages.error(request, "Inactive user.")
                return redirect(settings.BASE_URL + "account/")
            else:
                if get_data.otp == otp_code:
                    User.objects.filter(id=get_data.user.id).update(is_active=True)
                    VsUsers.objects.filter(id=user_id).update(otp=otp)
                    messages.info(request, 'Account Verify Successfully.')
                    
                    password = get_data.password
                    username = get_data.user.username
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        if user.is_superuser:
                            messages.error(request, "This login area is not used for superadmin.")
                        else:
                            if user.is_active:
                                login(request, user)
                                return redirect(settings.BASE_URL + "account/dashboard")
                            else:
                                messages.error(request, "Inactive user.")
                    return redirect(settings.BASE_URL+"account/")
                else:
                    messages.error(request, 'Your varification code is incorrect.')
        else:
            messages.error(request, 'Your user_id is incorrect.')
        user_code = request.POST["user_code"]
        return HttpResponseRedirect(reverse('account:varification',args=(user_code,)))


class RegistrationView(generic.View):
    d_user_form = SignUpForm
    vs_user_form = VsUsersForm

    def get(self,request):
        if request.user.username:
            return redirect(settings.BASE_URL)
        return render(request,"web/account/registration.html",{"d_user_form":self.d_user_form,"vs_user_form":self.vs_user_form})

    def post(self, request):
        if request.user.username:
            return redirect(settings.BASE_URL)
        post_data = request.POST or None
        d_user_form = self.d_user_form(post_data)
        vs_user_form = self.vs_user_form(post_data)

        if d_user_form.is_valid() and vs_user_form.is_valid():
            new_user = d_user_form.save(commit=False)
            new_user.is_active= False
            new_user.save()
            otp = ''.join([random.choice(string.digits) for i in range(0, 4)])
            vs_usr = vs_user_form.save(commit=False)
            vs_usr.user = new_user
            vs_usr.otp = otp
            vs_usr.password = request.POST["password1"]
            vs_usr.save()

            ################################################ EMAL SEND CODE START ##############
            get_system_info = VsSystemSettings.objects.all().first()
            data_content = { "yourname": vs_usr.name, "user_email": new_user.email,"otp": otp,"get_system_info":get_system_info,'user_code':vs_usr.user_code,"BASE_URL":settings.BASE_URL}
            email_content = render_to_string('email_template/email_send_for_create_new_account.html', data_content)
            msg = email.message.Message()
            msg['Subject'] = str(otp)+' is your OTP to verify and complete registration with iamRatedme.com'
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] =  new_user.email
            password = settings.EMAIL_HOST_PASSWORD
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(email_content)
            s = smtplib.SMTP(settings.EMAIL_HOST + ':' + str(settings.EMAIL_PORT))
            s.starttls()
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string())
            ################################################ EMAL SEND CODE END ##############
            messages.info(request, 'A Verification code has been sent to your email id.')
            return HttpResponseRedirect(reverse('account:varification',args=(vs_usr.user_code,)))
        else:
            messages.error(request, d_user_form.errors)
            messages.error(request, vs_user_form.errors)
        return render(request,"web/account/registration.html",{"d_user_form":d_user_form,"vs_user_form":vs_user_form})


class LoginView(generic.TemplateView):
    template_name = "web/account/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.username:
            return redirect(settings.BASE_URL)
        return context

def DashBoardView(request):
    get_data = None
    if request.user.is_superuser:
        return redirect(settings.BASE_URL + "admin")
    else:
        if VsUsers.objects.filter(user=request.user).exists():
            get_data = get_object_or_404(VsUsers , user=request.user)
            if VsUserSubscriptionPayment.objects.filter(User=get_data).filter(Active_status=True).exists():
                get_package_data = get_object_or_404(VsUserSubscriptionPayment, User=get_data, Active_status=True)
                if get_package_data:
                    if get_package_data.Expayer_date.date() >= datetime.today().date():
                        # return HttpResponse("test uhsdjbcdsahc dahc adshcb ds  sdc d")
                        return redirect(settings.BASE_URL + "dashboard/")
                    else:
                        # return HttpResponse("test uhsdjbcdsahc dahc adshcb ds  sdc d dfss")
                        return redirect(settings.BASE_URL + "subscription/")
                else:
                    # return HttpResponse("test uhsdjbcdsahc dahc adshcb ds  sdc d sdcdsc")
                    return redirect(settings.BASE_URL + "subscription/")
            else:
                return redirect(settings.BASE_URL + "subscription/")
    return redirect(settings.BASE_URL)

