from django.db import models
from django.contrib.auth.base_user import BaseUserManager


class UserQuerySet(models.QuerySet):

    def active(self):
        return self.filter(status="active")

    def blocked(self):
        return self.filter(status="blocked")

    def by_role(self, role_name):

        return self.filter(
            role__name__icontains=role_name
        )


class UserManager(BaseUserManager):

    def get_queryset(self):

        return UserQuerySet(
            self.model,
            using=self._db
        ).select_related("role")

    def active(self):

        return self.get_queryset().active()

    def blocked(self):

        return self.get_queryset().blocked()

    def by_role(self, role):

        return self.get_queryset().by_role(role)