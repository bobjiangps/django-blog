"""bobjiang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
##import ckeditor_uploader
from django.conf.urls.static import static
from django.conf import settings
from blog import views as blog_views
#import xadmin

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework import routers
from external.views import DebugViewSet
from external import views_auth_token as uat_views

router = routers.DefaultRouter()
# router.register(r'debug', DebugViewSet)

schema_view = get_schema_view(title='API DOC', renderer_classes=[SwaggerUIRenderer, OpenAPIRenderer])


urlpatterns = [
    path('bobjiang/admin/', admin.site.urls),
    #path('bobjiang/admin', xadmin.site.urls),
    path('', include('main.urls')),
    path('bobjiang/', include('blog.urls')),
    path('bobjiang/', include('comments.urls', namespace='comments')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('bobjiang/search/', include('haystack.urls')),
    path('tool/', include('tool.urls')),
    path('accounting/', include('accounting.urls')),
    # restful api below
    path('external/api/', include(router.urls)),
    # path('external/api/debug/', include('external.urls')),
    path('external/api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('external/api/api-token-auth/', uat_views.ObtainExpiringAuthToken.as_view(), name='api_token_auth'),
    path('external/api/login/', uat_views.ObtainExpiringAuthToken.as_view(), name='login'),
    path('external/api/logout/', uat_views.RevokeAuthToken.as_view(), name='logout'),
    path('external/api/docs/', schema_view, name='docs'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = blog_views.permission_denied
handler404 = blog_views.page_not_found
handler500 = blog_views.internal_error
