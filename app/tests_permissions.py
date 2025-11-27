import pytest
from rest_framework.test import APIRequestFactory

from app.permissions import GlobalDefaultPermission
from apps.genres.models import Genre


@pytest.mark.django_db
class TestGlobalDefaultPermission:
    def setup_method(self):
        self.permission = GlobalDefaultPermission()
        self.factory = APIRequestFactory()

    def test_has_permission_with_valid_view(self, user_with_permissions):
        request = self.factory.get('/genres/')
        request.user = user_with_permissions

        class MockView:
            queryset = Genre.objects.all()

        view = MockView()
        assert self.permission.has_permission(request, view) is True

    def test_has_permission_without_permissions(self, user_without_permissions):
        request = self.factory.get('/genres/')
        request.user = user_without_permissions

        class MockView:
            queryset = Genre.objects.all()

        view = MockView()
        assert self.permission.has_permission(request, view) is False

    def test_has_permission_with_invalid_view_no_queryset(self, user_with_permissions):
        request = self.factory.get('/test/')
        request.user = user_with_permissions

        class MockView:
            pass

        view = MockView()

        assert self.permission.has_permission(request, view) is False

    def test_has_object_permission_with_valid_view(self, user_with_permissions):
        request = self.factory.get('/genres/')
        request.user = user_with_permissions

        genre = Genre.objects.create(name='Action')

        class MockView:
            queryset = Genre.objects.all()

        view = MockView()
        assert self.permission.has_object_permission(request, view, genre) is True

    def test_has_object_permission_without_permissions(self, user_without_permissions):
        request = self.factory.get('/genres/')
        request.user = user_without_permissions

        genre = Genre.objects.create(name='Action')

        class MockView:
            queryset = Genre.objects.all()

        view = MockView()
        assert self.permission.has_object_permission(request, view, genre) is False

    def test_has_object_permission_with_invalid_view_no_queryset(self, user_with_permissions):
        request = self.factory.get('/test/')
        request.user = user_with_permissions

        genre = Genre.objects.create(name='Action')

        class MockView:
            pass

        view = MockView()
        assert self.permission.has_object_permission(request, view, genre) is False

    def test_get_action_suffix_for_all_methods(self):
        permission = GlobalDefaultPermission()

        assert permission._GlobalDefaultPermission__get_action_suffix('GET') == 'view'
        assert permission._GlobalDefaultPermission__get_action_suffix('POST') == 'add'
        assert permission._GlobalDefaultPermission__get_action_suffix('PUT') == 'change'
        assert permission._GlobalDefaultPermission__get_action_suffix('PATCH') == 'change'
        assert permission._GlobalDefaultPermission__get_action_suffix('DELETE') == 'delete'
        assert permission._GlobalDefaultPermission__get_action_suffix('OPTIONS') == 'view'
        assert permission._GlobalDefaultPermission__get_action_suffix('HEAD') == 'view'
        assert not permission._GlobalDefaultPermission__get_action_suffix('UNKNOWN')
