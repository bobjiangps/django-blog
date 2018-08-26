from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('about/', views.about_site_me, name='about_site_me'),
    path('article-01<int:post_id>/', views.post_detail, name='post_detail'),
    path('create-new/', views.create_new, name='create_new'),
    path('categorization/', views.archives, name='archives'),
    path('categorization/<int:year>/<int:month>/', views.archives_date, name='archives_date'),
    path('categorization/category/<str:category_name>/', views.archives_category, name='archives_category'),
    path('categorization/tag/<str:tag_name>/', views.archives_tag, name='archives_tag'),
]
