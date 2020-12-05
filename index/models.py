from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.db import transaction
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class PartManager(models.Manager):
    def get_query_set(self, user):
        qs = super(PartManager, self).get_queryset()
        if user.is_superuser:
            return qs
        return qs.filter(owner=user)

class Part(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    partno = models.CharField(max_length=100, unique=True)
    total = models.PositiveIntegerField(default=0)
    alarm = models.PositiveIntegerField(blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    shelf = models.CharField(max_length=20, blank=True, null=True)
    group = models.CharField(max_length=20, blank=True, null=True)
    price = models.DecimalField(
        default=0, max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0.0)])
    extra_info = models.CharField(max_length=500, blank=True, null=True)
    primary_order_address = models.EmailField(
        max_length=100, blank=True, null=True)
    secondary_order_address = models.EmailField(
        max_length=100, blank=True, null=True)

    objects = PartManager()

    class Meta:
        ordering = ("-created_at",)

    @transaction.atomic
    def plus(self):
        self.updated_at = timezone.now()
        self.total = self.total + 1
        self.save()

    @transaction.atomic
    def minus(self):
        self.updated_at = timezone.now()
        self.total = self.total - 1
        self.save()

    def search(user, q):
        return Part.objects.get_query_set(user).filter(Q(partno__icontains=q) |
                                    Q(shelf__icontains=q) |
                                    Q(group__icontains=q) |
                                    Q(description__icontains=q))
