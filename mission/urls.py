from django.urls import path
from . import views

urlpatterns = [
     path('mission/home/',
          views.MissionListView.as_view(),
          name='mission-home'),
     path('mission/new/',
          views.MissionCreateView.as_view(),
          name='mission-create'),
     path('mission/<int:pk>/',
          views.MissionDetailView.as_view(),
          name='mission-detail'),
     path('mission/<int:pk>/update',
          views.MissionUpdateView.as_view(),
          name='mission-update'),


]
