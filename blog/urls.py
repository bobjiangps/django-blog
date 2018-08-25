from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('article-01<int:post_id>/', views.post_detail, name='post_detail'),
    path('create-new/', views.create_new, name='create_new'),
    path('categorization/', views.archives, name='archives'),
    path('categorization/<int:year>/<int:month>/', views.archives_date, name='archives_date'),
]
