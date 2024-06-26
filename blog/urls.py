from django.urls import path
from . import views

urlpatterns = [
    path('', views.top_viewed_posts, name='top_viewed_posts'),
    path('post-list/', views.post_list, name='post_list'),
    # path('about_site_me/', views.about_site_me, name='about_site_me'),
    path('about-me/', views.about_me, name='about_me'),
    path('about-site/', views.about_site, name='about_site'),
    path('about-visitor/', views.about_visitor, name='about_visitor'),
    path('login/', views.do_login, name='do_login'),
    path('logout/', views.do_logout, name='do_logout'),
    path('post-list/sort-by-<str:sort_type>/', views.post_list_sort, name='post_list_sort'),
    path('article-01<int:post_id>/', views.post_detail, name='post_detail'),
    path('article-01<int:post_id>/edit', views.post_edit, name='post_edit'),
    path('create-new/', views.create_new, name='create_new'),
    path('categorization/', views.archives, name='archives'),
    path('categorization/<int:year>/<int:month>/', views.archives_date, name='archives_date'),
    path('categorization/<int:year>/<int:month>/sort-by-<str:sort_type>/', views.archives_date_sort, name='archives_date_sort'),
    path('categorization/category/<str:category_name>/', views.archives_category, name='archives_category'),
    path('categorization/category/<str:category_name>/sort-by-<str:sort_type>/', views.archives_category_sort, name='archives_category_sort'),
    path('categorization/tag/<str:tag_name>/', views.archives_tag, name='archives_tag'),
    path('categorization/tag/<str:tag_name>/sort-by-<str:sort_type>/', views.archives_tag_sort, name='archives_tag_sort'),
    path('show-view-record/', views.show_view_record, name='show_view_record'),
    path('download_bak/', views.download_bak, name='download_bak')
]
