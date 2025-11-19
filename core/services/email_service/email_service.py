from abc import ABC, abstractmethod

from django.conf import settings


class EmailService(ABC):
    FROM_EMAIL = settings.DEFAULT_FROM_EMAIL
    BACKGROUND_IMAGE = 'https://willsoftware-static.s3.us-east-1.amazonaws.com/img/flix_api_logo.jpg'

    def __init__(self, subject: str, message: str, to: list[str] = []) -> None:
        self.subject = subject
        self.message = message
        self.to = to

    @abstractmethod
    def send(self) -> None:
        raise NotImplementedError('Subclasses must implement this method')
