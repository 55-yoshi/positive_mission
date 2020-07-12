
from django.urls import path
from . import views

urlpatterns = [
    # ミッションにいいねアクセスしたとき
    path('mission/<int:pk>/good/', views.MissionGood, name='mission-good'),
    # 参加するにアクセスしたとき
    path('mission/<int:pk>/join/', views.MissionJoin, name='mission-join'),
    # ミッションクリアにアクセスしたとき
    path('mission/<int:pk>/success/', views.MissionSuccess, name='mission-success'),
    # ミッション承認にアクセスされたとき
    path('mission/<int:pk>/approval/', views.MissionApproval, name='mission-approval'),
    # サンクス承認にアクセスされたとき
    path('thanks/<int:pk>/approval/', views.ThanksApproval, name='thanks-approval'),
    # サンクスにいいねアクセスしたとき
    path('thanks/<int:pk>/good/', views.ThanksGood, name='thanks-good'),
]
