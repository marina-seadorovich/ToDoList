from django.db import models
# встроенная модель User
from django.contrib.auth.models import User


class Task(models.Model):
# many to one
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

# строковое представление модели
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']

# с помощью команды python manage.py makemigrations пеносим таблицу в БД
# с помощью команды python manage.py migrate создаем таблицы