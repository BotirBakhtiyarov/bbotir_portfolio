"""
Portfolio URL configuration. Clean URLs for SEO.
"""
from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.home, name='home'),
    path('cv/', views.cv_download, name='cv_download'),
    path('projects/', views.CaseStudyListView.as_view(), name='casestudy_list'),
    path('projects/<slug:slug>/', views.CaseStudyDetailView.as_view(), name='casestudy_detail'),
]
