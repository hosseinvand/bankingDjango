from django.contrib.auth.mixins import UserPassesTestMixin

from core.models import Manager


class SuperUserRequired(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class ManagerOrSuperUserRequired(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or hasattr(self.request.user, 'manager')


class ManagerRequired(UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'manager')