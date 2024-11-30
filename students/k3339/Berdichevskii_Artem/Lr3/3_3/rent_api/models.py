from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError


# Create your models here.
class RentUnit(models.Model):
    PERIOD_CHOICES = (
        ('st', 'days'),
        ('lt', 'months')
    )
    description = models.TextField()
    address = models.CharField(max_length=200)
    area_sq_m = models.IntegerField()
    cost = models.IntegerField()
    per_period = models.CharField(max_length=2, choices=PERIOD_CHOICES)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_displayed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Unit on {self.address} for {self.cost} per {self.per_period}'


class Lease(models.Model):
    rent_unit = models.ForeignKey(RentUnit, on_delete=models.CASCADE)
    dt_start = models.DateField()
    dt_end = models.DateField()
    tenant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    confirmed = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if self.dt_start > self.dt_end:
            raise ValidationError({
                'dt_end': 'End date must be greater than the start date.'
            })
        if self.rent_unit.owner == self.tenant:
            raise ValidationError({
                'rent_unit': 'Owner cannot be the same as tenant.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Lease on {self.rent_unit.address} for {self.tenant.username}'

class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    lease = models.OneToOneField(Lease, on_delete=models.CASCADE)

    description = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Rating must be between 1 and 10"
    )
    dt_published = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        if self.author != self.lease.tenant:
            raise ValidationError({
                "author": "Author must be the same as tenant in lease."
            })
        if not self.lease.confirmed:
            raise ValidationError({
                "lease": "Lease must first be confirmed."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Review from {self.author} for {self.lease.rent_unit.address}'