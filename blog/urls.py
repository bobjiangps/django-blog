from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    #path('about_site_me/', views.about_site_me, name='about_site_me'),
    path('about_me/', views.about_me, name='about_me'),
    path('about_site/', views.about_site, name='about_site'),
    path('login/', views.do_login, name='do_login'),
    path('logout/', views.do_logout, name='do_logout'),
    path('sort-by-<str:sort_type>/', views.post_list_sort, name='post_list_sort'),
    path('article-01<int:post_id>/', views.post_detail, name='post_detail'),
    path('article-01<int:post_id>/edit', views.post_edit, name='post_edit'),
    path('create-new/', views.create_new, name='create_new'),
    path('categorization/', views.archives, name='archives'),
    path('categorization/<int:year>/<int:month>/', views.archives_date, name='archives_date'),
    path('categorization/category/<str:category_name>/', views.archives_category, name='archives_category'),
    path('categorization/tag/<str:tag_name>/', views.archives_tag, name='archives_tag'),
]
