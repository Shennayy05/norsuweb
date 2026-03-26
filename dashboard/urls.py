from django.urls import path
from django.utils.autoreload import Path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index, name='home'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('super-admin-login/', views.super_admin_login, name='super_admin_login'),
    path('super-admin-dashboard/', views.super_admin_dashboard, name='super_admin_dashboard'),
    path('cas/', views.cas_dashboard, name='cas_dashboard'),
    path('cit/', views.cit_dashboard, name='cit_dashboard'),
    path('caf/', views.caf_dashboard, name='caf_dashboard'),
    path('cted/', views.cted_dashboard, name='cted_dashboard'),
    path('ccje/', views.ccje_dashboard, name='ccje_dashboard'),
    path('cba/', views.cba_dashboard, name='cba_dashboard'),
    path('news/', views.news, name='news'),
    path('news1/', views.news1, name='news1'),
    path('programs/', views.programs, name='programs'),
    path('alumni/', views.alumni, name='alumni'),
    path('alumni/about/', views.alumni_about, name='alumni_about'),
    path('alumni/achievements/', views.alumni_achievements, name='achievements'),
    path('alumni/careers/', views.alumni_careers, name='careers'),
    path('alumni/contact/', views.alumni_contact, name='contact'),
    path('directory/', views.alumni_directory, name='directory'),
    path('alumni/directory/', views.alumni_directory, name='directory_alumni'),
    path('alumni/events/', views.alumni_events, name='events'),
    path('alumni/gallery/', views.alumni_gallery, name='gallery'),
    path('alumni/programs/', views.alumni_programs, name='programs_alumni'),
    path('alumni/news/', views.alumni_news, name='news_alumni'),
    path('alumni/upload-media/', views.alumni_upload_media, name='upload_media'),
    path('alumnidasbord/', views.alumni_dashboard, name='alumni_dashboard'),
    # Post Management API endpoints
    path('api/posts/get/', views.get_posts, name='get_posts'),
    path('api/posts/create/', views.create_post, name='create_post'),
    path('api/posts/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    # Program Management API endpoints
    path('api/programs/', views.program_list_create, name='program_list_create'),
    path('api/programs/<int:pk>/', views.program_detail, name='program_detail'),
    # Faculty Management API endpoints
    path('api/faculty/', views.faculty_list_create, name='faculty_list_create'),
    path('api/faculty/<int:pk>/', views.faculty_delete, name='faculty_delete'),
    # Facility Management API endpoints
    path('api/facilities/', views.facility_list_create, name='facility_list_create'),
    path('api/facilities/<int:pk>/', views.facility_delete, name='facility_delete'),
    path('about/', views.aboutnorsu, name='about'),
    path('aboutnorsu-dashboard/', views.aboutnorsu_dashboard, name='aboutnorsu_dashboard'),
    path('academic-calendar/', views.academic_calendar, name='academic_calendar'),
    # Academic Calendar API endpoints
    path('api/calendar/', views.api_calendar_list_create, name='api_calendar_list_create'),
    path('api/calendar/<int:pk>/', views.api_calendar_detail, name='api_calendar_detail'),
    # Alumni API
    path('api/alumni/', views.alumni_api, name='alumni_api'),
    path('api/alumni/<int:pk>/', views.alumni_api, name='alumni_api_detail'),
    
    # Achievement API endpoints
    path('api/achievements/', views.achievement_list_create, name='achievement_list_create'),
    path('api/achievements/<int:pk>/', views.achievement_detail, name='achievement_detail'),
    # Alumni Success Story API endpoints
    path('api/success-stories/', views.success_story_list_create, name='success_story_list_create'),
    path('api/success-stories/<int:pk>/', views.success_story_detail, name='success_story_detail'),
    # Media Upload Management API endpoints
    path('api/media-uploads/', views.get_media_uploads, name='get_media_uploads'),
    path('api/media-uploads/<int:upload_id>/approve/', views.approve_media_upload, name='approve_media_upload'),
    path('api/media-uploads/<int:upload_id>/reject/', views.reject_media_upload, name='reject_media_upload'),
    path('api/media-uploads/<int:upload_id>/delete/', views.delete_media_upload, name='delete_media_upload'),
    
    # College Management API endpoints
    path('api/colleges/', views.college_list_create, name='college_list_create'),
    path('api/colleges/<int:pk>/', views.college_detail, name='college_detail'),
    path('api/alumni/about/', views.api_alumni_about, name='api_alumni_about'),
    path('api/alumni/news/', views.api_alumni_news, name='api_alumni_news'),
    path('api/alumni/news/<int:pk>/delete/', views.api_alumni_news_delete, name='api_alumni_news_delete'),
    path('api/alumni/events/', views.api_alumni_events, name='api_alumni_events'),
    path('api/alumni/events/<int:pk>/delete/', views.api_alumni_events_delete, name='api_alumni_events_delete'),
    path('aboutnosu/', views.aboutnorsu_dashboard, name='aboutnorsu_dashboard'),
]
