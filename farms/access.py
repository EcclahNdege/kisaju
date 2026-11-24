from .models import Farm

ALL_FARM_ROLES = ('owner', 'accountant')


def visible_farms(user):
    """Return the farms this user is allowed to see."""
    if user.role in ALL_FARM_ROLES:
        return Farm.objects.filter(is_active=True)
    if user.farm_id:
        return Farm.objects.filter(pk=user.farm_id, is_active=True)
    return Farm.objects.none()
