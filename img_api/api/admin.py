from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Customer, Tiers


@admin.register(Customer)
class Customer(admin.ModelAdmin):
    list_display = ('user', 'account_type',)
    ordering = ('user',)
    search_fields = ('user',)


@admin.register(Tiers)
class Tiers(admin.ModelAdmin):
    list_display = ('name', 'thumbnail_size', 'original_file', 'expiring_links')
    ordering = ('name',)
    search_fields = ('name',)

