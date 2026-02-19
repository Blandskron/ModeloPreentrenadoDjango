from django.contrib import admin
from .models import CreditRequest

@admin.register(CreditRequest)
class CreditRequestAdmin(admin.ModelAdmin):
    list_display = ("created_at", "client_name", "client_email", "status", "monto_maximo", "label")
    search_fields = ("client_name", "client_email", "status")
    list_filter = ("status", "label", "created_at")