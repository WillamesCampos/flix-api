from celery import shared_task
from django.core.mail import EmailMultiAlternatives

from app.settings import logger
from reviews.models import Review
from reviews.services.review_email_notification_service import ReviewEmailNotificationService


@shared_task
def send_review_email_notification(review_id):
    try:
        review = Review.objects.get(uuid=review_id)
        service = ReviewEmailNotificationService(EmailMultiAlternatives)
        service.send(review)
    except Review.DoesNotExist:
        logger_data = {
            'task': 'send_review_email_notification',
            'action': 'error',
            'review_id': review_id,
            'error_message': 'Review does not exist',
        }
        logger.error(logger_data)
    except Exception as e:
        logger_data = {
            'task': 'send_review_email_notification',
            'action': 'error',
            'review_id': review_id,
            'error_message': str(e),
        }
        logger.error(logger_data, exc_info=True)
