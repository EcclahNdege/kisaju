from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from farms.access import visible_farms

from .forms import DailyLogForm
from .models import DailyLog

RECORD_ROLES = ('owner', 'farm_manager', 'house_attendant')


@login_required
def log_list(request):
    logs = DailyLog.objects.filter(
        flock__house__farm__in=visible_farms(request.user)
    ).select_related('flock__house__farm')[:100]
    return render(request, 'production/log_list.html', {
        'logs': logs,
        'can_record': request.user.role in RECORD_ROLES,
    })


@login_required
def log_create(request):
    if request.user.role not in RECORD_ROLES:
        raise PermissionDenied
    form = DailyLogForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        log = form.save(commit=False)
        log.recorded_by = request.user
        log.save()
        messages.success(request, 'Daily log saved.')
        return redirect('log_list')
    return render(request, 'production/log_form.html', {'form': form})