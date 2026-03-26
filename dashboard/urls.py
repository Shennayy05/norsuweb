from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('cas/', views.cas_dashboard, name='cas_dashboard'),
    path('cit/', views.cit_dashboard, name='cit_dashboard'),
    path('caf/', views.caf_dashboard, name='caf_dashboard'),
    path('cted/', views.cted_dashboard, name='cted_dashboard'),
    path('ccje/', views.ccje_dashboard, name='ccje_dashboard'),
    path('cba/', views.cba_dashboard, name='cba_dashboard'),
    path('news/', views.news, name='news'),
    path('news1/', views.news1, name='news1'),
    path('programs/', views.programs, name='programs'),
    
]
