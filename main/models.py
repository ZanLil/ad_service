import os

from users.models import User
from django.db import models


class Ad(models.Model):
    """Модель объявления."""

    class Category(models.TextChoices):
        """Категории."""
        TANKS = 'Танки', 'Танки'
        HEALERS = 'Хилы', 'Хилы'
        DDS = 'ДД', 'ДД'
        MERCHANTS = 'Торговцы', 'Торговцы'
        GUILD_MASTERS = 'Гилдмастеры', 'Гилдмастеры'
        QUEST_GIVERS = 'Квестгиверы', 'Квестгиверы'
        BLACKSMITHS = 'Кузнецы', 'Кузнецы'
        TANNERS = 'Кожевники', 'Кожевники'
        POTION_MAKERS = 'Зельевары', 'Зельевары'
        SPELL_MASTERS = 'Мастера заклинаний', 'Мастера заклинаний'

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.TANKS)
    header = models.CharField(max_length=250)
    body = models.TextField()
    people_who_responded = models.ManyToManyField(User, related_name='peoples_who_responded', null=True, blank=True)
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='executor', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.author} - {self.header}'


class MediaFile(models.Model):
    """Модель медиа-файла."""
    ad = models.ForeignKey(Ad, related_name='media_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='ad_media/')

    def __str__(self):
        return f'{self.return_file_name()} - {self.ad.header}'

    def get_file_extension(self):
        """Возвращает расширение файла."""
        _, file_extension = os.path.splitext(self.file.name)
        return file_extension.lower()

    def return_file_name(self):
        """Возвращает 'Видео' или 'Изображение' в зависимости от расширения."""
        name = ''
        file_extension = self.get_file_extension()
        if file_extension == '.mp4':
            name = 'Видео'
        elif file_extension in ['.jpeg', '.jpg', '.png']:
            name = 'Изображение'
        return name


class Response(models.Model):
    """Модель отклика."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='responses')
    text = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.ad.header}'
