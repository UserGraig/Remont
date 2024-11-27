

from django.db import models
from django.utils import timezone


class Speciality(models.Model):
    name=models.CharField(max_length=200, unique=True)
    class Meta:
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"
    def __str__(self):
        return str(self.name)
    

class Client(models.Model):
    username = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=320)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
    def __str__(self):
        return str(self.username)

class Master(models.Model):
    username = models.CharField(max_length=200, unique=True)
    speciality =  models.ForeignKey(
        Speciality,
        on_delete=models.CASCADE,
        verbose_name="Специальность",
    )
    description = models.CharField(max_length=300)
    rating = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Рейтинг")
    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастеры"
    def __str__(self):
        return str(self.username)

class Order(models.Model):
    number=models.DecimalField(max_digits=3, decimal_places=0, verbose_name="Номер Заказа")
    id_user = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="ID клиента")
    id_master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name="ID мастера")
    create_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Цена")
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
    def __str__(self):
        return str(self.number)
    

