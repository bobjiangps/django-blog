from django.urls import path
from . import views

urlpatterns = [
    path('', views.tool_main_page, name='tool_main'),
    path('geoip', views.tool_geoip, name='tool_geoip'),
    path('useragent', views.tool_user_agent, name='tool_user_agent'),
    path('query', views.tool_query, name='tool_query')
]
