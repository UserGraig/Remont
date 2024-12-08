from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from .models import Client, Master, Order,Speciality, Service, Review

class MasterResource(resources.ModelResource):

    class Meta:

        model = Master
        fields = (
            "full_name",
            "description",
            "speciality",
            "rating",
        )
    def dehydrate_rating(self, obj):
        return f"{obj.rating:.2f}"
    def dehydrate_description(self, instance):
        return instance.description or "Описание отсутствует"
    
class ClientResource(resources.ModelResource):

    class Meta:

        model = Client
        fields = (
            "full_name",
            "email",
            "created_at",
        )

    def dehydrate_email(self, instance):
        return instance.email or "email не указан"


admin.site.register(Speciality)
admin.site.register(Order)

@admin.register(Client)
class ClientAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):

    resource_class = ClientResource
    list_display = ["full_name", "email", "created_at"]
    list_editable = ["email"]
    search_fields = ("full_name", "email")
    date_hierarchy = "created_at"

@admin.register(Master)
class MasterAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = MasterResource
    list_display = ["full_name", "speciality", "rating"]
    list_filter = ["speciality"]

@admin.register(Service)
class ServiceAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["name", "description"]
    list_editable = ["description"]
    search_fields = ["name", "description"]

@admin.register(Review)
class ReviewAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["client", "master", "rating", "comment", "created_at"]
    list_editable = ["comment"]
    search_fields = ["client", "master", "rating"]
    date_hierarchy = "created_at"






