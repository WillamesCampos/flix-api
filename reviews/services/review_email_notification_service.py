from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from app.settings import logger
from core.services.email_service.email_service import EmailService
from reviews.models import Review


class ReviewEmailNotificationService(EmailService):
    REVIEW_NOTIFICATION_SUBJECT = 'New Review Notification'
    REVIEW_NOTIFICATION_MESSAGE = 'A new review has been submitted for the movie {movie_title}.'
    REVIEW_NOTIFICATION_TEMPLATE = 'reviews/email/review_notification.html'

    def __init__(self, sender_email: EmailMessage) -> None:
        self.sender_email = sender_email
        super().__init__(subject=self.REVIEW_NOTIFICATION_SUBJECT, message=self.REVIEW_NOTIFICATION_MESSAGE)

    def __build_message(self, review: Review) -> str:
        logger_data = {
            'service': 'ReviewEmailNotificationService',
            'method': 'send',
            'subject': self.subject,
            'message': self.message,
            'movie_title': review.movie.title,
            'review_comment': review.comment,
            'review_stars': review.stars,
            'review_created_at': review.created_at,
            'review_updated_at': review.updated_at,
            'review_created_by': review.created_by,
            'review_updated_by': review.updated_by,
        }
        logger.info(logger_data)

        self.to = [review.created_by.email]

        context = {
            'movie_title': review.movie.title,
            'review_comment': review.comment,
            'review_stars': review.stars,
            'template_message': self.REVIEW_NOTIFICATION_MESSAGE.format(movie_title=review.movie.title),
            'subject': self.REVIEW_NOTIFICATION_SUBJECT,
            'background_image_url': self.BACKGROUND_IMAGE,
        }

        html_body = render_to_string(self.REVIEW_NOTIFICATION_TEMPLATE, context)

        return html_body

    def send(self, review: Review) -> None:
        html_body = self.__build_message(review)

        email = self.sender_email(subject=self.REVIEW_NOTIFICATION_SUBJECT, body=html_body, from_email=self.FROM_EMAIL, to=self.to)

        email.attach_alternative(content=html_body, mimetype='text/html')

        try:
            email.send()
            logger_data = {
                'service': 'ReviewEmailNotificationService',
                'action': 'sent',
                'subject': self.REVIEW_NOTIFICATION_SUBJECT,
                'to': self.to,
                'error': None,
            }
            logger.info(logger_data)
        except Exception as e:
            logger_data = {
                'service': 'ReviewEmailNotificationService',
                'action': 'failed',
                'subject': self.REVIEW_NOTIFICATION_SUBJECT,
                'to': self.to,
                'error_message': str(e),
            }
            logger.error(logger_data, exc_info=True)
            raise e
