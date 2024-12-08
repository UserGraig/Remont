

from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords


class Speciality(models.Model):
    name=models.CharField(max_length=200, unique=True)
    history = HistoricalRecords()
    class Meta:
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"
    def __str__(self):
        return str(self.name)
    

class Client(models.Model):
    full_name = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=320, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    history = HistoricalRecords()
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
    def __str__(self):
        return str(self.full_name)

class Master(models.Model):
    full_name = models.CharField(max_length=200, unique=True)
    speciality =  models.ForeignKey(
        Speciality,
        on_delete=models.CASCADE,
        verbose_name="Специальность",
    )
    description = models.CharField(max_length=300, blank=True, verbose_name="Описание")
    rating = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Рейтинг")
    history = HistoricalRecords()
    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастеры"
    def __str__(self):
        return str(self.full_name)

class Order(models.Model):
    number=models.DecimalField(max_digits=3, decimal_places=0, verbose_name="Номер Заказа")
    id_user = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="ID клиента")
    id_master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name="ID мастера")
    create_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Цена")
    history = HistoricalRecords()
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
    def __str__(self):
        return str(self.number)


# ------------------------Nouvelle table pour Service
class Service(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=500)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
    
    def __str__(self):
        return str(self.name)

# Nouvelle table pour Review
class Review(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name="Мастер")
    rating = models.DecimalField(max_digits=2, decimal_places=1, verbose_name="Рейтинг")
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
    
    def __str__(self):
        return f"Отзыв {self.id} для {self.master}"



