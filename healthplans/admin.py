from .models import Provider
from .models import Plan
from django.contrib import admin

class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', )
    search_fields = ('name', 'website', )
    ordering = ('name', )
    prepopulated_fields = {'slug': ('name',)}

class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_rate', )
    search_fields = ('name', )
    ordering = ('name', 'category')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Provider, ProviderAdmin)
admin.site.register(Plan, PlanAdmin)
