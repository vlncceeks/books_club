from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .managers import UserManager
from django.urls import reverse

class Role(models.Model):
    name = models.CharField(
        "Название роли",
        max_length=50,
        unique=True
    )
    description = models.TextField(
        "Описание роли",
        blank=True
    )

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"
        ordering = ["name"]

    def __str__(self):
        return self.name


class User(AbstractUser):
    manager = UserManager()
    STATUS_CHOICES = [
        ("active", "Активный"),
        ("blocked", "Заблокирован"),
        ("inactive", "Неактивный"),
    ]

    role = models.ForeignKey(
        Role,
        verbose_name="Роль",
        on_delete=models.PROTECT,
        related_name="users"
    )

    birth_date = models.DateField(
        "Дата рождения",
        null=True,
        blank=True
    )

    bio = models.TextField(
        "О себе",
        blank=True
    )

    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    updated_at = models.DateTimeField(
        "Дата обновления",
        auto_now=True
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.username} ({self.role.name})"
    

    def get_absolute_url(self):
        return reverse(
            "user-profile",
            kwargs={"user_id": self.id}
        )

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def get_books_by_status(self, status):
        return self.user_books.filter(reading_status=status)
    
    def get_events_by_status(self, status=None):
        """
        Получить мероприятия пользователя по статусу
        status: 'future', 'past', 'today', 'soon'
        """
        now = timezone.now()
        events = self.events.all()  
        
        if status == 'future':
            return events.filter(event_date__gt=now)
        elif status == 'past':
            return events.filter(event_date__lt=now)
        elif status == 'today':
            return events.filter(
                event_date__date=now.date()
            )
        elif status == 'soon':
            week_later = now + timezone.timedelta(days=7)
            return events.filter(
                event_date__gt=now,
                event_date__lte=week_later
            )
        return events