from django.db import models
from django.core.exceptions import ValidationError
from books.models import Book
from django.utils import timezone
from users.models import User

class Event(models.Model):
    title = models.CharField("Название встречи", max_length=200)
    description = models.TextField("Описание", blank=True)

    event_date = models.DateTimeField("Дата и время")

    book = models.ForeignKey(
        Book,
        verbose_name="Обсуждаемая книга",
        on_delete=models.PROTECT,
        related_name="events"
    )

    organizer = models.ForeignKey(
        User,
        verbose_name="Организатор",
        on_delete=models.PROTECT,
        related_name="organized_events"
    )

    participants = models.ManyToManyField(
        User,
        verbose_name="Участники",
        blank=True,
        related_name="events"
    )

    max_participants = models.PositiveIntegerField(
        "Максимальное количество мест"
    )

    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        "Дата изменения",
        auto_now=True
    )

    class Meta:
        verbose_name = "Встреча"
        verbose_name_plural = "Встречи"
        ordering = ["-event_date"]
        indexes = [
            models.Index(fields=['event_date']),
        ]

    def __str__(self):
        return f"{self.title} ({self.event_date.strftime('%d.%m.%Y %H:%M')})"

    @property
    def registered_count(self):
        return self.participants.count()

    @property
    def free_places(self):
        return self.max_participants - self.registered_count
    
    @property
    def is_full(self):
        return self.registered_count >= self.max_participants

    def clean(self):
        if self.pk and self.registered_count > self.max_participants:
            raise ValidationError(
                "Количество участников превышает лимит мест."
            )
    @property
    def is_past(self):
        """Мероприятие уже прошло"""
        return timezone.now() > self.event_date

    @property
    def is_future(self):
        """Мероприятие еще не наступило"""
        return timezone.now() < self.event_date
    
    @property
    def is_soon(self):
        """Мероприятие скоро наступит"""
        if self.event_date > timezone.now():
            return (self.event_date - timezone.now()).days <= 3
        return False
    
    @property
    def is_ongoing(self):
        """Мероприятие происходит сейчас (в течение часа)"""
        now = timezone.now()
        return self.event_date <= now <= self.event_date + timezone.timedelta(hours=1)
    
    @property
    def status(self):
        """Статус мероприятия"""
        if self.is_past:
            return "past"
        elif self.is_full:
            return "full"
        elif self.is_soon:
            return "soon"
        else:
            return "available"

    @property
    def status_display(self):
        """Отображение статуса на русском"""
        statuses = {
            "past": "Прошло",
            "full": "Мест нет",
            "soon": "Скоро",
            "available": "Есть места"
        }
        return statuses.get(self.status)
    

    # Методы для записи/отмены записи
    def can_register(self, user):
        """Проверка, может ли пользователь записаться"""
        if self.is_past:
            return False, 
        if self.is_full:
            return False, 
        if self.participants.filter(id=user.id).exists():
            return False, 
        if user.status != 'active':
            return False, 
        return True, "Можно записаться"

    def register_user(self, user):
        can_register, message = self.can_register(user)
        
        if not can_register:
            raise ValidationError(message)
        
        self.participants.add(user)
        
        return True, f"Вы успешно записаны на мероприятие '{self.title}'"

    def unregister_user(self, user):
        if not self.participants.filter(id=user.id).exists():
            raise ValidationError("Вы не записаны на это мероприятие")
        
        if self.is_past:
            raise ValidationError("Нельзя отменить запись на прошедшее мероприятие")
        
        self.participants.remove(user)
        
        return True, f"Запись на мероприятие '{self.title}' отменена"
    