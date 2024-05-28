from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer
from utils.permission import HasAssignedPermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from users.views_auth_token import ObtainExpiringAuthToken


class UserViewSet(viewsets.ModelViewSet):
    """
        get:
            Return all users.

        post:
            Create a new user.

        put:
            Update a user.

        patch:
            Update one or more fields on an existing user.

        delete:
            Delete existing user.
    """
    permission_classes = [HasAssignedPermission]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "email"]


class Me(APIView):
    """
    Get ony API, used to return the permission map for the current used logged in.
    """

    queryset = User.objects.none()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        permission = ObtainExpiringAuthToken.list_perms(user=user)
        permissions_dict = {'permissions': permission, 'admin': self.is_admin(permission)}
        return Response(permissions_dict)

    @staticmethod
    def is_admin(permission):
        if 'create' in permission['group'] and 'create' in permission['user']:
            return True
        else:
            return False
