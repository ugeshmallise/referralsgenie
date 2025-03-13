from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('register-jobprovider/', views.register_jobprovider, name='register_jobprovider'),
    path('login-jobprovider/', views.login_jobprovider, name='login_jobprovider'),
    path('logout-jobseeker/', views.logout_user, name='logout-jobseeker'),
    path('jobseeker-guestlogin/', views.jobseeker_guest_login, name='jobseeker-guestlogin'),
    path('jobseeker-guestlogout/', views.jobseeker_guest_logout, name='jobseeker-guestlogout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)