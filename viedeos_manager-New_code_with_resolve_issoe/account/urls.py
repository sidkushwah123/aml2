from django.urls import path
from . import views
from django.contrib.auth import views as auth_login

urlpatterns = [
    path('', auth_login.LoginView.as_view(template_name='web/account/login.html',redirect_authenticated_user=True),name="login"),
    path('logout', auth_login.LogoutView.as_view() ,name="logout"),

    path('test_mail', views.test_mail ,name="test_mail"),


    

    path('registration', views.RegistrationView.as_view(),name="registration"),
    path('<slug:user_code>/varification', views.VarificationView.as_view(),name="varification"),
    path('<slug:user_id>/send-otp', views.Send_opt,name="send_otp"),

    path('dashboard', views.DashBoardView ,name="dashboard"),


    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_login.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_login.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_login.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_login.PasswordResetConfirmView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_confirm'),
    path('password_reset/', auth_login.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_login.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),
]