from django.urls import path
from . import views

urlpatterns = [
    # path('debug', views.DebugViewSet.as_view(), name='debug_api'),
    path('call_stat/', views.CallStatList.as_view(), name='call_stat_list'),
    path(r'call_stat/<int:pk>/', views.CallStatDetail.as_view(), name='call_stat_detail'),
]
