from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cas/', views.cas_dashboard, name='cas_dashboard'),
    path('cit/', views.cit_dashboard, name='cit_dashboard'),
    path('caf/', views.caf_dashboard, name='caf_dashboard'),
    path('cted/', views.cted_dashboard, name='cted_dashboard'),
    path('ccje/', views.ccje_dashboard, name='ccje_dashboard'),
    path('cba/', views.cba_dashboard, name='cba_dashboard'),

]
