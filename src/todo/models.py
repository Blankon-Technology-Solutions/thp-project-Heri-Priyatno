import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from account.models import User

logger = logging.getLogger()


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Todo)
def update_todo(sender, instance: Todo, **kwargs):
    logger.info(f"POST SAVE: {instance.title}")
    channel_layer = get_channel_layer()
    todo_group = f"todo_{slugify(instance.user.email)}"
    async_to_sync(channel_layer.group_send)(todo_group, {"type": "todo.update"})
