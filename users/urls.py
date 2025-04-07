from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import  JobPostingListView
from .views import ContactSupportView, ResolveTicketView
from .views import JobPostingView


urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('register-jobprovider/', views.register_jobprovider, name='register_jobprovider'),
    path('login-jobprovider/', views.login_jobprovider, name='login_jobprovider'),
    path('logout-jobseeker/', views.logout_user, name='logout-jobseeker'),
    path('jobseeker-guestlogin/', views.jobseeker_guest_login, name='jobseeker-guestlogin'),
    path('jobseeker-guestlogout/', views.jobseeker_guest_logout, name='jobseeker-guestlogout'),
    path('jobs/', JobPostingView.as_view(), name='job-create-bulk'),  # For creating single/multiple jobs
    path('jobs/<uuid:job_id>/', JobPostingView.as_view(), name='job-update-delete'),  # For updating & deleting     
    path('list-jobs/', JobPostingListView.as_view(), name='list-jobs'),
    path('support/', ContactSupportView.as_view(), name='create_support_ticket'),  # POST: Create a ticket, GET: List by email
    path('support/<uuid:ticket_id>/', ContactSupportView.as_view(), name='get_support_ticket'),  # GET: Retrieve a ticket
    path('support/<uuid:ticket_id>/resolve/', ResolveTicketView.as_view(), name='resolve_support_ticket'),  # PATCH: Resolve a ticketz

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)