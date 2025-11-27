from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.reviews.models import Review
from apps.reviews.tasks import send_review_email_notification


@receiver(post_save, sender=Review)
def send_review_email_notification_signal(sender, instance, created, **kwargs):
    if created:
        send_review_email_notification.delay(str(instance.uuid))
