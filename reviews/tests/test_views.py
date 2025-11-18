import uuid

import pytest
from django.urls import reverse
from rest_framework import status

from app.tests import BaseAPITest
from movies.tests.factories import MovieFactory
from reviews.models import Review
from reviews.tests.factories import ReviewFactory


@pytest.fixture
def review_data():
    movie = MovieFactory()
    return {
        'movie': movie.uuid,
        'stars': 5,
        'comment': 'Great movie!',
    }


@pytest.fixture
def existing_review():
    return ReviewFactory()


@pytest.mark.django_db
class TestReviewAPI(BaseAPITest):
    def test_list_reviews_success(self, existing_review):
        self.give_permissions(model=Review)

        ReviewFactory.create_batch(5)

        url = reverse('review-create-list')
        response = self.client.get(url, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == Review.objects.count()

    def test_list_reviews_without_permissions(self, existing_review):
        url = reverse('review-create-list')
        response = self.client.get(url, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_reviews_user_not_authenticated(self, existing_review):
        self.client.logout()
        url = reverse('review-create-list')

        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_review_success(self, review_data):
        self.give_permissions(model=Review)

        url = reverse('review-create-list')
        response = self.client.post(url, review_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Review.objects.count() == 1
        assert Review.objects.get().stars == review_data['stars']

    def test_create_review_without_permissions(self, review_data):
        url = reverse('review-create-list')
        response = self.client.post(url, review_data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_review_user_not_authenticated(self, review_data):
        self.client.logout()
        url = reverse('review-create-list')

        response = self.client.post(url, review_data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_review_success(self, existing_review):
        self.give_permissions(model=Review)

        url = reverse('review-detail-view', kwargs={'pk': existing_review.pk})
        response = self.client.get(url, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['stars'] == existing_review.stars

    def test_retrieve_review_not_found(self):
        self.give_permissions(model=Review)

        url = reverse('review-detail-view', kwargs={'pk': uuid.uuid4()})
        response = self.client.get(url, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_review_without_permissions(self, existing_review):
        url = reverse('review-detail-view', kwargs={'pk': existing_review.pk})
        response = self.client.get(url, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_review_user_not_authenticated(self, existing_review):
        self.client.logout()
        url = reverse('review-detail-view', kwargs={'pk': existing_review.pk})

        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_review_success(self, existing_review):
        self.give_permissions(model=Review)

        updated_data = {'stars': 4, 'comment': 'Updated comment'}
        url = reverse('review-detail-view', kwargs={'pk': existing_review.pk})

        response = self.client.put(url, updated_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        existing_review.refresh_from_db()
        assert existing_review.stars == updated_data['stars']

    def test_update_review_without_permissions(self, existing_review):
        updated_data = {'stars': 4, 'comment': 'Updated comment'}
        url = reverse('review-detail-view', kwargs={'pk': existing_review.pk})

        response = self.client.put(url, updated_data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_review_user_not_authenticated(self, existing_review):
        self.client.logout()
        updated_data = {'stars': 4, 'comment': 'Updated comment'}
        url = reverse('review-detail-view', kwargs={'pk': existing_review.pk})

        response = self.client.put(url, updated_data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_review_success(self, existing_review):
        self.give_permissions(model=Review)

        url = reverse('review-detail-view', kwargs={'pk': existing_review.pk})
        response = self.client.delete(url, format='json')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Review.objects.filter(pk=existing_review.pk).exists()

    def test_delete_review_not_found(self):
        self.give_permissions(model=Review)

        url = reverse('review-detail-view', kwargs={'pk': uuid.uuid4()})
        response = self.client.delete(url, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_review_without_permissions(self, existing_review):
        url = reverse('review-detail-view', kwargs={'pk': existing_review.pk})
        response = self.client.delete(url, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_review_user_not_authenticated(self, existing_review):
        self.client.logout()
        url = reverse('review-detail-view', kwargs={'pk': existing_review.pk})

        response = self.client.delete(url, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
