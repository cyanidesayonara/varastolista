from django.contrib import admin
from .models import Part


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('partno', 'total', 'created_at', 'updated_at')
    fields = ('partno', 'total')

