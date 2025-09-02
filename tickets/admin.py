from django.contrib import admin

# Register your models here.
# tickets/admin.py
from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'customer', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('subject', 'description')
