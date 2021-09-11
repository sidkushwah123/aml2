from django.shortcuts import render,get_object_or_404,HttpResponseRedirect,redirect
from django.views import generic
from account.models import VsUsers
from account.forms import VsUsersForm
from datetime import datetime
from datetime import date
from django.core.files.base import ContentFile
import base64
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls import reverse
from imratedme import settings
# Create your views here.

@method_decorator(login_required , name="dispatch")
class ProfileView(SuccessMessageMixin,generic.CreateView):
    template_name = "web/profile/profile.html"
    form_class = VsUsersForm
    success_url = reverse_lazy('profiles:profile')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_data  = None
        if VsUsers.objects.filter(user=self.request.user).exists():
            get_data = get_object_or_404(VsUsers , user=self.request.user)

        get_form = VsUsersForm(instance=get_data)
        context["form"] = get_form
        context["user_info"] = get_data

        return context



    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            # return HttpResponseRedirect(reverse('admin_manage_setting:update_general',args=(get_data.id,)))
            return redirect(settings.BASE_URL+"admin/")
        else:
            return super(ProfileView, self).dispatch(request, *args, **kwargs)


    def get_success_message(self, cleaned_data):
        # print(cleaned_data)
        return "Profile update successfully."
    def form_valid(self, form):
        get_object = get_object_or_404(VsUsers, user=self.request.user)
        get_object.name= self.request.POST["name"]
        get_object.Zip_Code= self.request.POST["Zip_Code"]
        get_object.Contact_no= self.request.POST["Contact_no"]
        if self.request.POST["user_image"]:
            format, imgstr = self.request.POST["user_image"].split(';base64,')
            ext = format.split('/')[-1]
            dateTimeObj = datetime.now()
            today_date = date.today()
            set_file_name = str(today_date.day) + "_" + str(today_date.month) + "_" + str(today_date.year) + "_" + str(
                dateTimeObj.microsecond)
            file_name = set_file_name + "." + ext
            data = ContentFile(base64.b64decode(imgstr), name=file_name)
            get_object.Image.delete(save=False)
            get_object.Image = data
        get_object.save()
        messages.info(self.request,"Profile Updated Successfully")
        return HttpResponseRedirect(reverse('profiles:profile'))

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return HttpResponseRedirect(reverse('profiles:profile'))