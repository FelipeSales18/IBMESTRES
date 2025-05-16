from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Projeto, Team
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .serializers import ProjectSerializer, TeamSerializer

@receiver(post_save, sender=Projeto)
def project_saved(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    data = ProjectSerializer(instance).data
    async_to_sync(channel_layer.group_send)(
        "projects", {"type": "project.update", "data": data}
    )

@receiver(post_save, sender=Team)
def team_saved(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    data = TeamSerializer(instance).data
    async_to_sync(channel_layer.group_send)(
        "teams", {"type": "team.update", "data": data}
    )