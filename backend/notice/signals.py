from django.db.models.signals import post_save
from django.dispatch import receiver
from detailview.models import Party
from .tasks import create_new_party_notice

@receiver(post_save, sender=Party)
def send_new_party_notice(sender, instance, created, **kwargs):
    if created:
        create_new_party_notice.delay(instance.id)
