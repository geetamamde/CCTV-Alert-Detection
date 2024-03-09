
from django.urls import path
from . import views 



urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.signup),
    path('login',views.login_view,name='login'),
    path('signout',views.signout),
    path('change-password/', views.change_password, name='change_password'),
    path('change-password2/', views.change_password2, name='change_password2'),
    path('verify/<slug:token>',views.verify),
]

