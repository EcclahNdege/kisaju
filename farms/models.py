from django.db import models
from django.utils import timezone


class Farm(models.Model):
    class FarmType(models.TextChoices):
        LAYERS = 'layers', 'Layers (eggs)'
        BROILERS = 'broilers', 'Broilers (meat)'

    name = models.CharField(max_length=100, unique=True)
    farm_type = models.CharField(max_length=10, choices=FarmType.choices)
    location = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class House(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.PROTECT, related_name='houses')
    name = models.CharField(max_length=50, help_text='e.g. H3')
    capacity = models.PositiveIntegerField(help_text='Maximum number of birds')

    class Meta:
        ordering = ['farm', 'name']
        constraints = [
            models.UniqueConstraint(fields=['farm', 'name'], name='unique_house_per_farm')
        ]

    def __str__(self):
        return f'{self.farm} - {self.name}'


class Flock(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        CLOSED = 'closed', 'Closed'

    house = models.ForeignKey(House, on_delete=models.PROTECT, related_name='flocks')
    code = models.CharField(max_length=30, unique=True, help_text='e.g. ISI-2026-01')
    breed = models.CharField(max_length=100)
    initial_quantity = models.PositiveIntegerField()
    arrival_date = models.DateField(default=timezone.localdate)
    age_at_arrival_days = models.PositiveIntegerField(default=1)
    cost_per_bird = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        ordering = ['-arrival_date']

    def __str__(self):
        return f'{self.code} ({self.house})'