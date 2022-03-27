from django.contrib import admin
from .models import Task

# регистрируем модель Таск с помощью админ панели Джанго

admin.site.register(Task)
