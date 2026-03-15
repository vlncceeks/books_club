from django.db import models
from django.utils import timezone
from users.models import User

class Genre(models.Model):
    name = models.CharField("Название жанра", max_length=50, unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ['name']

    def __str__(self):
        return self.name



class Book(models.Model):
    title = models.CharField("Название книги", max_length=200)
    description = models.TextField("Описание", blank=True, null=True)
    author = models.CharField("Автор", max_length=100)
    genre = models.ForeignKey(Genre, verbose_name="Жанр", on_delete=models.PROTECT, related_name='books')
    year = models.PositiveIntegerField("Год издания", blank=True, null=True)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['title', 'author'] 
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return f"{self.title} ({self.author})"


# Связь пользователь - книга
class UserBook(models.Model):
    READING_STATUS_CHOICES = [
        ('want', 'Хочу прочитать'),
        ('reading', 'Читаю'),
        ('read', 'Прочитал(a)')
    ]
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name='user_books')
    book = models.ForeignKey(Book, verbose_name="Книга", on_delete=models.CASCADE, related_name='user_books')
    reading_status = models.CharField("Статус чтения", max_length=15, 
        choices=READING_STATUS_CHOICES,
        default='want'  
    )
    rating = models.PositiveSmallIntegerField("Оценка", blank=True, null=True)

    # Даты начала и окончания чтения
    started_reading_at = models.DateTimeField("Начало чтения", blank=True, null=True)
    finished_reading_at = models.DateTimeField("Окончание чтения", blank=True, null=True)
    
    created_at = models.DateTimeField("Дата добавления в список", auto_now_add=True)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True)

    class Meta:
        verbose_name = "Статус книги пользователя"
        verbose_name_plural = "Статусы книг пользователей"
        unique_together = ('user', 'book')
        ordering = ['-created_at'] 

    def __str__(self):
        return f"{self.user.username} → {self.book.title}"
    
    def start_reading(self):
        """Начать чтение книги"""
        if self.reading_status == 'want':
            self.reading_status = 'reading'
            self.started_reading_at = timezone.now()
            self.save()
    
    def finish_reading(self, rating=None):
        """Завершить чтение книги"""
        if self.reading_status == 'reading':
            self.reading_status = 'read'
            self.finished_reading_at = timezone.now()
            if rating:
                self.rating = rating
            self.save()
    
    def reading_duration_days(self):
        """Длительность чтения в днях"""
        if self.started_reading_at and self.finished_reading_at:
            delta = self.finished_reading_at - self.started_reading_at
            return delta.days
        elif self.started_reading_at and self.reading_status == 'reading':
            delta = timezone.now() - self.started_reading_at
            return delta.days
        return 0
    
    def get_comments(self):
        return self.comments.all()

