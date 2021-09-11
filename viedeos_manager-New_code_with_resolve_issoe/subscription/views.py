from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import VsUserSubscriptionPayment,VsSubscription,VsPayPal
from datetime import date
from datetime import datetime,timedelta
from django.contrib import messages
from django.db.models import Q
from account.models import VsUsers
from manage_coupons.models import AwCuponCode
from django.http import HttpResponse, JsonResponse
from dateutil.relativedelta import relativedelta
from imratedme import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def check_coupon(request):
    status = "0"
    message = "Invalid method"
    data = {}
    if request.method == 'POST':
        order_id = request.POST['order_id']
        coupon_code = request.POST['coupon_code']
        if AwCuponCode.objects.filter(CouponCode=coupon_code).exists():     # check is avelabel or not
            get_code_ins = get_object_or_404(AwCuponCode, CouponCode=coupon_code)
            if get_code_ins.Valid_from <= datetime.today().date():
                if get_code_ins.Valid_to >= datetime.today().date():
                    if VsUserSubscriptionPayment.objects.filter(order_id=order_id).exists():
                        get_order  = get_object_or_404(VsUserSubscriptionPayment,order_id=order_id)
                        get_all_use_coupon_count = 0
                        get_count_of_use_coupon_code_by_one_user = 0
                        if VsUserSubscriptionPayment.objects.filter(Descount_coupon=get_code_ins).filter(User__user=request.user).exists():
                            get_count_of_use_coupon_code_by_one_user_data = VsUserSubscriptionPayment.objects.filter(Descount_coupon=get_code_ins).filter(User__user=request.user)
                            get_count_of_use_coupon_code_by_one_user = len(get_count_of_use_coupon_code_by_one_user_data)
                        if VsUserSubscriptionPayment.objects.filter(Descount_coupon=get_code_ins).exists():
                            get_all_use_coupon_count_data = VsUserSubscriptionPayment.objects.filter(Descount_coupon=get_code_ins)
                            get_all_use_coupon_count = len(get_all_use_coupon_count_data)

                        if get_code_ins.Usage_Limit_Per_Coupon > get_all_use_coupon_count:
                            if get_code_ins.Usage_Limit_Per_User > get_count_of_use_coupon_code_by_one_user:
                                VsUserSubscriptionPayment.objects.filter(order_id=order_id).update(Descount_coupon=get_code_ins)
                                status = "1"
                                amount = get_order.Amount
                                if get_code_ins.Type.lower() == 'p':
                                    get_descount_amount = (amount*get_code_ins.Amount) / 100
                                else:
                                    get_descount_amount = get_code_ins.Amount

                                amount_after_descount_rount_fig = round(amount - get_descount_amount, 2)
                                VsUserSubscriptionPayment.objects.filter(order_id=order_id).update(Amount_after_descount=amount_after_descount_rount_fig)
                                data["amount_after_descount"] = round(amount - get_descount_amount, 2)
                                data["order_id"] = get_order.order_id
                                message = "Coupon Code applay successgurlly."
                            else:
                                message = "Can not use again."
                        else:
                            message = "code use limit are end."
                    else:
                        message = "order_id is incorrect."
                else:
                    message = "Coupon Code is expayer."
            else:
                message = "This code is not usefull at this time."
        else:
            message = "Incorrect Code."
    return JsonResponse({"status":status,"message":message,"data":data})

def add_package(request,package_id):
    status = "0"
    message= ""
    data = ""
    if VsSubscription.objects.filter(id=package_id).exists():
        get_package_ins = get_object_or_404(VsSubscription,id=package_id)
        Amount_set = get_package_ins.Price * 3
        if VsUsers.objects.filter(user=request.user).exists():
            get_vs_user_instance = get_object_or_404(VsUsers,user=request.user)
            active_starts = False
            upload_limit = 0
            if get_package_ins.Price < 1:
                upload_limit =  get_package_ins.Upload_Video_limit
                VsUserSubscriptionPayment.objects.filter(User=get_vs_user_instance).filter(Package_name=get_package_ins).update(
                    Active_status=False)
                active_starts =  True
            currentDate = datetime.now()
            end_date = currentDate + relativedelta(months=1)
            add_data = VsUserSubscriptionPayment(Package_name=get_package_ins,Upload_Video_limit=upload_limit,User=get_vs_user_instance,Buy_date=datetime.now(),Amount=Amount_set,Active_status=active_starts,Expayer_date=end_date)
            add_data.save()
            data = {"order_id":add_data.order_id,"amount":add_data.Amount}
            status = "1"
            message = "Order add successfully."
        else:
            status = "0"
            message = "User is incorrect."
    else:
        status = "0"
        message = "package id is incorrect."
    return JsonResponse({"status": status, "message": message,"data":data})





def update_package(request,order_id,id):
    status = "0"
    message= ""
    if VsUserSubscriptionPayment.objects.filter(order_id=order_id).exists():
        get_order =  get_object_or_404(VsUserSubscriptionPayment,order_id=order_id)
        VsUserSubscriptionPayment.objects.filter(~Q(order_id=order_id)).filter(User=get_order.User).update(Active_status=False)
        currentDate = datetime.now()
        if get_order.Package_name.Free_trial:
            if VsUserSubscriptionPayment.objects.filter(~Q(order_id=order_id)).filter(User=get_order.User).filter(Package_name=get_order.Package_name).exists():
                end_date = currentDate + relativedelta(months=3)
            else:
                end_date = currentDate + relativedelta(months=4)
        else:
            end_date = currentDate + relativedelta(months=3)
        upload_limit = 0
        if get_order.Package_name.Upload_Video_limit:
            upload_limit = get_order.Package_name.Upload_Video_limit
        VsUserSubscriptionPayment.objects.filter(order_id=order_id).update(Upload_Video_limit=upload_limit,Buy_date=datetime.now(),Start_date=datetime.now(),Expayer_date=end_date,Payment_status=True,Active_status=True,Payment_method="PayPal",Transaction_id=id)
        status = "1"
        message = "Payment Successful."
    else:
        message = "Order_id is incorrect."
    return JsonResponse({"status": status, "message": message})


@method_decorator(login_required , name="dispatch")
class MySubscriptionPageView(generic.TemplateView):
    template_name = "web/subscription/my_subscription.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_package_info =None
        get_vs_user_instance = get_object_or_404(VsUsers,user=self.request.user)
        user_package = None
        if VsUserSubscriptionPayment.objects.filter(User=get_vs_user_instance).filter(Active_status=True).exists():
            user_package = get_object_or_404(VsUserSubscriptionPayment,User=get_vs_user_instance,Active_status=True)
        context['user_package']=user_package
        return context

class SubscriptionPageView(generic.TemplateView):
    template_name = "web/subscription/subscription.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_package_info =None
        if VsSubscription.objects.all().exists():
            get_package_info = VsSubscription.objects.all().order_by("id")
        context['get_package_info']=get_package_info
        paypal_id=VsPayPal.objects.all().last()
        context['paypal_id']=paypal_id.PayPal_Clientid
        context['BASE_URL']=settings.BASE_URL
        get_user_current_plan = None
        if self.request.user.is_authenticated:
            get_vs_user_instance = get_object_or_404(VsUsers, user=self.request.user)
            message = ""
            if VsUserSubscriptionPayment.objects.filter(User=get_vs_user_instance).filter(Active_status=True).exists():
                # get_user_current_plan = get_object_or_404(VsUserSubscriptionPayment, User=get_vs_user_instance, Active_status=True)
                get_user_current_plan = VsUserSubscriptionPayment.objects.filter(User=get_vs_user_instance).filter(Active_status=True).last()
                if get_user_current_plan.Expayer_date.date() < datetime.today().date():
                    messages.error(self.request, "Your Package is expayer.")
            else:
                messages.error(self.request, "Please choose at least one plan.")
        context['get_user_current_plan'] = get_user_current_plan
        return context