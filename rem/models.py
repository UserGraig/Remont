from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

class Speciality(models.Model):
    """
    Модель специальности.

    Эта модель представляет специальности, которые могут быть назначены мастерам.

    Атрибуты:
        name (str): Название специальности, должно быть уникальным.
        history (HistoricalRecords): Хранит историю изменений объектов.
    """
    name = models.CharField(max_length=200, unique=True)
    history = HistoricalRecords()

    class Meta:
        """
        Метаданные модели специальности.

        Атрибуты:
            verbose_name (str): Человекочитаемое название модели в единственном числе.
            verbose_name_plural (str): Человекочитаемое название модели во множественном числе.
        """
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"

    def __str__(self):
        """
        Возвращает строковое представление объекта специальности.
        """
        return str(self.name)

class Client(models.Model):
    """
    Модель клиента.

    Эта модель представляет клиентов, которые могут оставлять отзывы и делать заказы.

    Атрибуты:
        full_name (str): Полное имя клиента, должно быть уникальным.
        email (str): Электронная почта клиента, может быть пустым.
        created_at (datetime): Дата и время создания записи о клиенте.
        history (HistoricalRecords): Хранит историю изменений объектов.
    """
    full_name = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=320, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    history = HistoricalRecords()

    class Meta:
        """
        Метаданные модели клиента.

        Атрибуты:
            verbose_name (str): Человекочитаемое название модели в единственном числе.
            verbose_name_plural (str): Человекочитаемое название модели во множественном числе.
        """
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        """
        Возвращает строковое представление объекта клиента.
        """
        return str(self.full_name)

class Master(models.Model):
    """
    Модель мастера.

    Эта модель представляет мастеров, которые могут выполнять услуги.

    Атрибуты:
        full_name (str): Полное имя мастера, должно быть уникальным.
        speciality (ForeignKey): Ссылка на объект специальности, к которой относится мастер.
        description (str): Описание мастера, может быть пустым.
        rating (Decimal): Рейтинг мастера, с максимальной длиной 10 и двумя знаками после запятой.
        history (HistoricalRecords): Хранит историю изменений объектов.
    """
    full_name = models.CharField(max_length=200, unique=True)
    speciality = models.ForeignKey(
        Speciality,
        on_delete=models.CASCADE,
        verbose_name="Специальность",
    )
    description = models.CharField(max_length=300, blank=True, verbose_name="Описание")
    rating = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Рейтинг")
    history = HistoricalRecords()

    class Meta:
        """
        Метаданные модели мастера.

        Атрибуты:
            verbose_name (str): Человекочитаемое название модели в единственном числе.
            verbose_name_plural (str): Человекочитаемое название модели во множественном числе.
        """
        verbose_name = "Мастер"
        verbose_name_plural = "Мастеры"

    def __str__(self):
        """
        Возвращает строковое представление объекта мастера.
        """
        return str(self.full_name)

class Order(models.Model):
    """
    Модель заказа.

    Эта модель представляет заказы, сделанные клиентами у мастеров.

    Атрибуты:
        number (Decimal): Номер заказа.
        id_user (ForeignKey): Ссылка на клиента, который сделал заказ.
        id_master (ForeignKey): Ссылка на мастера, который выполнит заказ.
        create_at (datetime): Дата и время создания заказа.
        updated_at (datetime): Дата и время последнего обновления заказа.
        price (Decimal): Цена заказа.
        history (HistoricalRecords): Хранит историю изменений объектов.
    """
    number = models.DecimalField(max_digits=3, decimal_places=0, verbose_name="Номер Заказа")
    id_user = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="ID клиента")
    id_master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name="ID мастера")
    create_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Цена")
    history = HistoricalRecords()

    class Meta:
        """
        Метаданные модели заказа.

        Атрибуты:
            verbose_name (str): Человекочитаемое название модели в единственном числе.
            verbose_name_plural (str): Человекочитаемое название модели во множественном числе.
        """
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        """
        Возвращает строковое представление объекта заказа.
        """
        return str(self.number)

class Service(models.Model):
    """
    Модель услуги.

    Эта модель представляет услуги, которые могут быть предоставлены мастерами.

    Атрибуты:
        name (str): Название услуги, должно быть уникальным.
        description (str): Описание услуги.
    """

    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=500)

    class Meta:
        """
        Метаданные модели услуги.

        Атрибуты:
            verbose_name (str): Человекочитаемое название модели в единственном числе.
            verbose_name_plural (str): Человекочитаемое название модели во множественном числе.
        """
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
    
    def __str__(self):
        """
        Возвращает строковое представление объекта услуги.
        """
        return str(self.name)

class Review(models.Model):
    """
    Модель отзыва.

    Эта модель представляет отзывы клиентов о мастерах.

    Атрибуты:
        client (ForeignKey): Ссылка на клиента, который оставил отзыв.
        master (ForeignKey): Ссылка на мастера, о котором оставлен отзыв.
        rating (Decimal): Рейтинг, присвоенный мастеру клиентом.
        comment (TextField): Комментарий клиента.
        created_at (datetime): Дата и время создания отзыва.
    """

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name="Мастер")
    rating = models.DecimalField(max_digits=2, decimal_places=1, verbose_name="Рейтинг")
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """
        Метаданные модели отзыва.

        Атрибуты:
            verbose_name (str): Человекочитаемое название модели в единственном числе.
            verbose_name_plural (str): Человекочитаемое название модели во множественном числе.
        """
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
    
    def __str__(self):
        """
        Возвращает строковое представление объекта отзыва.
        """
        return f"Отзыв {self.id} для {self.master}"

class Task(models.Model):
    """ Exemple de modèle pour représenter une tâche """
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
