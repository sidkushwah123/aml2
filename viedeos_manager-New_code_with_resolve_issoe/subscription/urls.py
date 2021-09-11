from django.urls import path
from . import views

urlpatterns = [
    path('', views.SubscriptionPageView.as_view(), name="subscription"),
    path('my-subscription', views.MySubscriptionPageView.as_view(), name="mysubscription"),
    path('add-package/<slug:package_id>', views.add_package, name="add_package"),
    path('update-package/<slug:order_id>/<slug:id>', views.update_package, name="update_package"),
    path('check-coupon/', views.check_coupon, name="check_coupon"),
]