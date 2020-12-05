from import_export import resources, fields
from django.contrib.auth.models import User
from import_export.widgets import ForeignKeyWidget
from .models import Part

class PartResource(resources.ModelResource):
    owner = fields.Field(
        column_name='owner',
        attribute='owner',
        widget=ForeignKeyWidget(User, 'username'))

    class Meta:
        model = Part
