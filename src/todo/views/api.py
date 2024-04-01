from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from todo.models import Todo
from todo.serializers import TodoSerializer


class IsTodoOwner(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(self.has_permission(request, view) and obj.user == request.user)


class TodoApiView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = [IsTodoOwner, ]
    filterset_fields = ['completed',]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        return qs.filter(user=self.request.user)

    def finalize_response(self, request, response, *args, **kwargs):
        channel_layer = get_channel_layer()
        user = self.request.user
        group_name = f'todo_{user.email}'
        # Trigger message sent to group
        # async_to_sync(channel_layer.group_send)(
        #     group_name, {
        #         "type": "todo.update",
        #         "message": "Update"
        #     }
        # )
        return super().finalize_response(request, response, *args, **kwargs)


