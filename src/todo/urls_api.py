from rest_framework import routers

from todo.views import api

router = routers.DefaultRouter()
router.register(r'todos', api.TodoApiView, 'todo')

urlpatterns = router.urls