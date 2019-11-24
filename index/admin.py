from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib import admin
from .models import Part


@admin.register(Part)
class PartAdmin(ImportExportModelAdmin):
    list_display = ('partno', 'total', 'created_at', 'owner', 'updated_at', 'description',
                    'location', 'shelf', 'group', 'price', 'extra_info', 'primary_order_address', 'secondary_order_address')
    fields = ('partno', 'total', 'description', 'owner',
                    'location', 'shelf', 'group', 'price', 'extra_info', 'primary_order_address', 'secondary_order_address')
            
class PartResource(resources.ModelResource):
    class Meta:
        model = Part
