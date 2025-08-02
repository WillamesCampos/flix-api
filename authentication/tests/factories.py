import factory
from django.contrib.auth import get_user_model

from app.test_settings import faker_gen

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.LazyAttribute(lambda username: faker_gen.user_name())
    email = factory.LazyAttribute(lambda email: faker_gen.email())
    password = factory.PostGenerationMethodCall('set_password')

    class Meta:
        model = User
