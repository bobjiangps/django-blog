from .models import Account
from .serializers import AccountSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response


class AccountViewSet(viewsets.ModelViewSet):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        # limit the returned data only belongs to current user, cannot view/update another user's account
        queryset = Account.objects.filter(user_id=self.request.user.id).order_by("id")
        return queryset

    # 如果想禁用某一个方法，可以类似如下，但不如用generics.RetrieveUpdateAPIView
    def destroy(self, request, *args, **kwargs):
        return Response({"message": "delete action is not allowed to 'Account'", "code": "400"}, status=status.HTTP_400_BAD_REQUEST)
