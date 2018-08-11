from django.urls import path
from . import views


app_name = 'comments'
urlpatterns = [
    path('comment/article-01<int:post_id>/', views.post_comment, name='post_comment'),
]
