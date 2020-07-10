from django.urls import path
from . import views

urlpatterns = [
    path('thanks/list/', views.ThanksListView.as_view(), name='thanks-list'),
    path('thanks/create/', views.ThanksCreateView.as_view(), name='thanks-create'),
    path('thanks/<int:pk>/', views.ThanksDetailView.as_view(), name='thanks-detail'),
]