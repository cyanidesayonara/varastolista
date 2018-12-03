from import_export import resources
from .models import Part

class PartResource(resources.ModelResource):
    class Meta:
        model = Part
