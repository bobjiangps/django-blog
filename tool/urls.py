from django.urls import path
from . import views

urlpatterns = [
    path('', views.tool_main_page, name='tool_main')
]
