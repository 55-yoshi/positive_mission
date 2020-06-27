
from django.urls import path
from . import views

urlpatterns = [
    # いいねにアクセスしたとき
    path('mission/<int:pk>/like/', views.MissionGood, name='mission-good'),
    # 参加するにアクセスしたとき
    path('mission/<int:pk>/join/', views.MissionJoin, name='mission-join'),
    # ミッションクリアにアクセスしたとき
    path('mission/<int:pk>/gain/', views.MissionSuccess, name='mission-success'),
    
]
