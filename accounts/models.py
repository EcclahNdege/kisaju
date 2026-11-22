from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        OWNER = 'owner', 'Owner (Admin)'
        ACCOUNTANT = 'accountant', 'Accountant'
        FARM_MANAGER = 'farm_manager', 'Farm Manager'
        STOREKEEPER = 'storekeeper', 'Storekeeper'
        HOUSE_ATTENDANT = 'house_attendant', 'House Attendant'
        SALES_CASHIER = 'sales_cashier', 'Sales / Cashier'

    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.HOUSE_ATTENDANT
    )
    phone = models.CharField(max_length=20, blank=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Role.OWNER
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'