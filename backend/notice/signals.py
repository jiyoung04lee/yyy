from django.db.models.signals import post_save
from django.dispatch import receiver
from detailview.models import Party
from .tasks import create_new_party_notice

@receiver(post_save, sender=Party)
def send_new_party_notice(sender, instance, created, **kwargs):
    if created:
        # 개발/로컬 확인용
        create_new_party_notice(instance.id)  
        # 운영에서는 create_new_party_notice.delay(instance.id)
