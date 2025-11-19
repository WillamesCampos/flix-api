from django.db.models.signals import post_save
from django.dispatch import receiver

from reviews.models import Review
from reviews.services.review_email_notification_service import review_email_notification_service


@receiver(post_save, sender=Review)
def send_review_email_notification(sender, instance, created, **kwargs):
    if created:
        review_email_notification_service.send(instance)
