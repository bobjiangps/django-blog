from django.utils import timezone
from django.contrib.auth.models import User
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
import datetime


class ObtainExpiringAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            utc_now = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
            user.last_login = utc_now
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            if request.path_info.find("/logout/") > 0:
                token.delete()
                return Response({"token": "deleted"})
            if not created:
                if token.created < utc_now - datetime.timedelta(hours=72):
                    print("re-generate token for old one is expired")
                    token.delete()
                    token = Token.objects.create(user=user)
                    token.created = datetime.datetime.utcnow()
                    token.save()
                else:
                    token.created = datetime.datetime.utcnow()
                    token.save()
            if request.path_info.find("/login/") > 0:
                return Response({"id": user.pk,
                                 "username": user.username,
                                 "mail": user.email,
                                 "token": token.key})
            else:
                return Response({"token": token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def list_perms(user):
        exclude_list = ["token", "contenttype", "session", "logentry"]
        readonly_list = ["permission"]
        user_perms_dict = {}
        user_perms_list = []
        for am in apps.get_models():
            name = am.__name__.lower()
            if name not in exclude_list:
                user_perms_dict[name] = []
                user_perms_list.append(name)
        default_all_perms = user.get_all_permissions()
        for perm in default_all_perms:
            new_perm = perm.split(".")[-1]
            action, module = new_perm.split("_")
            action_new_name = {"add": "create",
                               "change": "update",
                               "view": "read"}
            if action == "delete" and module in ["user"]:
                continue
            if action in action_new_name.keys():
                action = action_new_name[action]
            if module in readonly_list and action == "read":
                user_perms_dict[module] = [action]
            if module not in exclude_list and module not in readonly_list:
                if module in user_perms_list:
                    if action not in user_perms_dict[module]:
                        user_perms_dict[module].append(action)
                else:
                    user_perms_dict[module] = [action]
                    user_perms_list.append(module)
        for d in user_perms_dict.keys():
            user_perms_dict[d].sort()
        return user_perms_dict


class RevokeAuthToken(APIView):
    queryset = User.objects.none()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        return Response({"result": "Successfully logged out."}, status=status.HTTP_200_OK)
