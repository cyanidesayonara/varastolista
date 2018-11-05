from django.db import models
from django.utils import timezone

# Create your models here.
class Part(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    partno = models.CharField(primary_key=True, max_length=100)
    total = models.IntegerField(default=0)

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
