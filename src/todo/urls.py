from django.urls import path

from todo.views import HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="todo-home"),
]
