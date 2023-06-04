from .models import Debug, CalledStat
from rest_framework import viewsets
from .serializers import DebugSerializer, CallStatSerializer
from rest_framework import generics
from rest_framework import filters
from django.utils import timezone


def record_api_called_stat(name):
    api_stat_exist = CalledStat.objects.filter(name=name)
    if api_stat_exist:
        current_api = api_stat_exist[0]
        current_api.increase_views()
    else:
        current_api = CalledStat()
        current_api.name = name
        today = timezone.now()
        current_api.create_date = today
        current_api.update_date = today
        current_api.amount = 1
        current_api.save()


class DebugViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    # record_api_called_stat("Debug")
    queryset = Debug.objects.all().order_by("id")
    serializer_class = DebugSerializer

    def dispatch(self, request, *args, **kwargs):
        record_api_called_stat("Debug")
        return super().dispatch(request, *args, **kwargs)


class CallStatList(generics.ListCreateAPIView):
    """
        get:
            Return all object.

        post:
            Create a new object.
    """
    queryset = CalledStat.objects.all().order_by("-id")
    serializer_class = CallStatSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def dispatch(self, request, *args, **kwargs):
        record_api_called_stat(self.__class__.__name__)
        return super().dispatch(request, *args, **kwargs)


class CallStatDetail(generics.RetrieveUpdateAPIView):
    """
        get:
            Return a object instance.

        put:
            Update a object.

        patch:
            Update one or more fields on an existing object.

    """
    queryset = CalledStat.objects.all()
    serializer_class = CallStatSerializer

    def dispatch(self, request, *args, **kwargs):
        record_api_called_stat(self.__class__.__name__)
        return super().dispatch(request, *args, **kwargs)
