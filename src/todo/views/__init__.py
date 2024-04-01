from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView

from todo.models import Todo


# Create your views here.

class HomePageView(LoginRequiredMixin, ListView):
    template_name = "home.html"

    def get_queryset(self):
        """Return all the latest todos."""
        return Todo.objects.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        title = request.POST['title']

        Todo.objects.create(title=title, user=self.request.user)

        return redirect('todo-home')

