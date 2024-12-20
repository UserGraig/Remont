"""
Этот модуль реализует админ-панель для проекта Django.
"""

from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from .models import Client, Master, Order, Speciality, Service, Review


class MasterResource(resources.ModelResource):
    """
    Ресурс для экспорта данных о мастерах.

    Этот класс предоставляет возможность экспортировать данные о мастерах
    в различных форматах, таких как CSV, JSON, XLSX и др.

    Атрибуты:
        model: Модель Master, которая будет использоваться для экспорта.
        fields: Список полей, которые будут включены в экспорт.

    Методы:
        dehydrate_rating(self, obj): Форматирует рейтинг мастера с точностью
        до двух знаков после запятой.

        dehydrate_description(self, instance): Возвращает описание мастера
        или "Описание отсутствует", если оно не задано.
    """

    class Meta:
        """
        Настройки для экспорта данных о мастерах.

        Атрибуты:
            model: Модель Master, которая будет использоваться для экспорта.
            fields: Список полей, которые будут включены в экспорт.
        """

        model = Master
        fields = (
            "full_name",
            "description",
            "speciality",
            "rating",
        )

    def dehydrate_rating(self, obj):
        """
        Форматирует рейтинг мастера для вывода.
        Строка с форматированным рейтингом, округлённым до двух знаков после запятой.
        """
        return f"{obj.rating:.2f}"

    def dehydrate_description(self, instance):
        """
        Возвращает описание мастера.
        Строка с описанием мастера. Если описание отсутствует, возвращает "Описание отсутствует".
        """
        return instance.description or "Описание отсутствует"


class ClientResource(resources.ModelResource):
    """
    Ресурс для экспорта данных о клиентах.

    Этот класс предоставляет возможность экспортировать данные о клиентах
    в различных форматах, таких как CSV, JSON, XLSX и др.

    Атрибуты:
        model: Модель Client, которая будет использоваться для экспорта.
        fields: Список полей, которые будут включены в экспорт.

    Методы:
        dehydrate_email(self, instance): Возвращает email клиента
        или "email не указан", если он отсутствует.
    """

    class Meta:
        """
        Настройки для экспорта данных о клиентах.

        Атрибуты:
            model: Модель Client, которая будет использоваться для экспорта.
            fields: Список полей, которые будут включены в экспорт.
        """

        model = Client
        fields = (
            "full_name",
            "email",
            "created_at",
        )

    def dehydrate_email(self, instance):
        """
        Возвращает email клиента.
        Строка с email клиента. Если email отсутствует, возвращает "email не указан".
        """
        return instance.email or "email не указан"


admin.site.register(Speciality)
admin.site.register(Order)

@admin.register(Client)
class ClientAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    """
    Класс для управления клиентами в админ-панели.
    """

    resource_class = ClientResource
    list_display = ["full_name", "email", "created_at"]
    list_editable = ["email"]
    search_fields = ("full_name", "email")
    date_hierarchy = "created_at"


@admin.register(Master)
class MasterAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    """
    Класс для управления мастерами в админ-панели.
    """

    resource_class = MasterResource
    list_display = ["full_name", "speciality", "rating"]
    list_filter = ["speciality"]


@admin.register(Service)
class ServiceAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    """
    Класс для управления услугами в админ-панели.
    """

    list_display = ["name", "description"]
    list_editable = ["description"]
    search_fields = ["name", "description"]


@admin.register(Review)
class ReviewAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    """
    Класс для управления отзывами в админ-панели.
    """

    list_display = ["client", "master", "rating", "comment", "created_at"]
    list_editable = ["comment"]
    search_fields = ["client", "master", "rating"]
    date_hierarchy = "created_at"
    raw_id_fields = ('client', 'master')
