from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .access import visible_farms


@login_required
def dashboard(request):
    farms = visible_farms(request.user).prefetch_related('houses__flocks')
    return render(request, 'dashboard.html', {'farms': farms})