from django.contrib.auth.mixins import UserPassesTestMixin

from core.models import Manager


class SuperUserRequired(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class ManagerRequired(UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'manager')