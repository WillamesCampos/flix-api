import faker
from rest_framework.test import APIClient
from rest_framework.test import APITestCase


class BaseTestCase(APITestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        self.client = APIClient()

        self.faker = faker.Faker(locale='en_US')

    def generate_male_name(self):
        self.faker.given_name_male()

    def generate_female_name(self):
        self.faker.given_name_female()
