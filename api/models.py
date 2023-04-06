from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    
    USERNAME_FIELD = 'username'
    
    username = models.CharField("Короткая ссылка", max_length=15, unique=True)
    email = models.EmailField("Почта", unique=True)
    password = models.CharField("Пароль", max_length=128)
    description = models.TextField("Описание профиля")
    first_name = models.CharField("Имя", max_length=15)
    last_name = models.CharField("Фамилия", max_length=20)

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"
