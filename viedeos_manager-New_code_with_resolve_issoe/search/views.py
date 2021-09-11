from django.shortcuts import render,get_object_or_404,redirect
from django.views import generic
from videos.models import VsVideos
from django.http import HttpResponse, JsonResponse
from videos.models import VsRating
from django.db.models import CharField, Value,Count
from django.db.models import Sum
from django.db.models import OuterRef, Subquery
from categorys_and_reatings.models import VsCategory,VsSubCategoryes
from django.template.defaulttags import register
from django.template.loader import render_to_string
from .serializers import GetVideoSerializers
from django.db.models import Q
from imratedme import settings
# Create your views here.

@register.simple_tag
def get_sub_catogory(categorye,search_cate="",search_sub_cate=""):
    
    cate_count = 0
    if VsVideos.objects.filter(Categoryes=categorye).exists():
        cate_count = VsVideos.objects.filter(Categoryes=categorye).count();

    sub_cate = None
    if VsSubCategoryes.objects.filter(Status=True).filter(Category=categorye).exists():
        sub_cate = VsSubCategoryes.objects.filter(Status=True).filter(Category=categorye)
    content = {"items":categorye,"cate_count":cate_count,"sub_cate":sub_cate,"search_cate":search_cate,"search_sub_cate":search_sub_cate}
    return render_to_string('web/search/categor_and_sub.html',content)



def search_item(request):
    item  = request.GET["q"]
    get_data = {}
    if VsVideos.objects.filter(Publich_Status=True).filter(Q(Videos_Slug__contains=item)|Q(Meta_Title__contains=item)|Q(Meta_keyword__contains=item)).exists():
        get_videos = VsVideos.objects.filter(Publich_Status=True).filter(Q(Videos_Slug__contains=item)|Q(Meta_Title__contains=item)|Q(Meta_keyword__contains=item))[:5]
        get_data_sri = GetVideoSerializers(get_videos, many=True)
        get_data=get_data_sri.data
    return JsonResponse(get_data,safe=False)




class SearchView(generic.ListView):
    template_name = "web/search/search.html"
    model = VsVideos
    queryset = None
    paginate_by = 12

    def get_queryset(self, **kwargs):
        set_order_by = "-id"
        if "shorting" in self.request.GET:
            if self.request.GET["shorting"] == "latest":
                set_order_by = "-id"
            if self.request.GET["shorting"] == "oldest":
                 set_order_by = "id"
            if self.request.GET["shorting"] == "most-rated":
                set_order_by = "-Reating"
        get_search_result = VsVideos.objects.filter(Publich_Status=True).order_by(set_order_by)
        # ================= add filter for keyword end ===================================
        if "keyword" in self.request.GET:
            keyword= self.request.GET["keyword"]
            # get_search_result = VsVideos.objects.filter(Publich_Status=True ,Videos_Slug__contains=keyword).order_by(set_order_by)
            get_search_result = VsVideos.objects.filter(Publich_Status=True).filter(Q(Videos_Slug__contains=keyword)|Q(Meta_Title__contains=keyword)|Q(Meta_keyword__contains=keyword)).order_by(set_order_by)
        #======================================ADD FILTER FOR CATEFORY START ================ 
        # ================= add filter for keyword start ===================================
        
        
        category_filter = ""
        if "category" in self.request.GET:
            get_cate_slug= self.request.GET["category"]
            if VsCategory.objects.filter(Status=True).filter(Slug=get_cate_slug).exists():
                category =  get_object_or_404(VsCategory , Status=True,Slug=get_cate_slug)
                if "sub-categorye" in self.request.GET:
                     get_sub_cate_slug= self.request.GET["sub-categorye"]
                     if VsSubCategoryes.objects.filter(Status=True).filter(Slug=get_sub_cate_slug).filter(Category=category).exists():
                        sub_category =  get_object_or_404(VsSubCategoryes , Status=True,Slug=get_sub_cate_slug,Category=category)
                        get_search_result = VsVideos.objects.filter(Publich_Status=True,Categoryes=category,Sub_Categoryes=sub_category).order_by(set_order_by)
                else:
                    get_search_result = VsVideos.objects.filter(Publich_Status=True,Categoryes=category).order_by(set_order_by)
        #======================================ADD FILTER FOR CATEFORY end ================      
        return get_search_result


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            # return HttpResponseRedirect(reverse('admin_manage_setting:update_general',args=(get_data.id,)))
            return redirect(settings.BASE_URL+"admin/")
        else:
            return super(SearchView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Category = None
        shorting = ""
        if "shorting" in self.request.GET:
            shorting = self.request.GET["shorting"]

        search_cate = ""
        if "category" in self.request.GET:
            search_cate = self.request.GET["category"]
        # print(context)
        search_sub_sate = ""
        if "sub-categorye" in self.request.GET:
            search_sub_sate= self.request.GET["sub-categorye"]
        category = None
        if VsCategory.objects.filter(Status=True).exists():
            category = VsCategory.objects.filter(Status=True)
        keyword = ""
        if "keyword" in self.request.GET:
            keyword= self.request.GET["keyword"]
        context["category"] = category
        context["search_sub_sate"] = search_sub_sate
        context["shorting"] = shorting
        context["search_cate"] = search_cate
        context["keyword"] = keyword
        context["shorting_content"] = {"latest":"Latest","oldest":"Oldest","most-rated":"Most Rated"}
        return context