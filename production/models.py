from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class DailyLog(models.Model):
    flock = models.ForeignKey(
        'farms.Flock', on_delete=models.PROTECT, related_name='daily_logs'
    )
    date = models.DateField(default=timezone.localdate)
    deaths = models.PositiveIntegerField(default=0)
    culls = models.PositiveIntegerField(default=0)
    feed_used_kg = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    eggs_collected = models.PositiveIntegerField(null=True, blank=True)
    avg_weight_kg = models.DecimalField(
        max_digits=5, decimal_places=3, null=True, blank=True,
        help_text='Broilers: average sample weight',
    )
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'flock']
        constraints = [
            models.UniqueConstraint(fields=['flock', 'date'], name='one_log_per_flock_per_day')
        ]

    def __str__(self):
        return f'{self.flock.code} on {self.date}'

    def clean(self):
        if not self.flock_id:
            return
        flock = self.flock
        farm_type = flock.house.farm.farm_type

        if self.date:
            if self.date > timezone.localdate():
                raise ValidationError('The date cannot be in the future.')
            if self.date < flock.arrival_date:
                raise ValidationError('The date is before this flock arrived.')

        if flock.status != flock.Status.ACTIVE:
            raise ValidationError('This flock is closed.')

        available = flock.live_birds
        if self.pk:
            old = DailyLog.objects.get(pk=self.pk)
            available += old.deaths + old.culls
        if (self.deaths or 0) + (self.culls or 0) > available:
            raise ValidationError(f'Only {available} birds are left in this flock.')

        if self.eggs_collected is not None and farm_type != 'layers':
            raise ValidationError('Eggs can only be recorded for layer flocks.')
        if self.avg_weight_kg is not None and farm_type != 'broilers':
            raise ValidationError('Weights can only be recorded for broiler flocks.')