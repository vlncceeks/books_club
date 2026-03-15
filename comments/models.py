from django.db import models
from books.models import Book
from users.models import User
from events.models import Event

class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name="Книга", blank=True, null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, verbose_name="Встреча", blank=True, null=True, on_delete=models.CASCADE)
    text = models.TextField("Текст комментария")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        target = self.book.title if self.book else self.event.title if self.event else "Не указано"
        return f"{self.user.username} → {target}"
