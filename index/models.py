from django.db import models
from django.utils import timezone

# Create your models here.
class Part(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    partno = models.CharField(max_length=100, unique=True)
    total = models.IntegerField(default=0)
    description = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    shelf = models.CharField(max_length=20, blank=True)
    group = models.CharField(max_length=20, blank=True)
    price = models.DecimalField(default=0, max_digits=9, decimal_places=2, blank=True)
    extra_info = models.CharField(max_length=500, blank=True)
    primary_order_address = models.EmailField(max_length=100, blank=True)
    secondary_order_address = models.EmailField(max_length=100, blank=True)

    class Meta:
        ordering = ("-updated_at",)

    def update(self):
        self.updated_at = timezone.now()
        self.save()

    def plus(self):
        self.updated_at = timezone.now()
        self.total = self.total + 1

    def minus(self):
        if self.total > 0:
            self.updated_at = timezone.now()
            self.total = self.total - 1
