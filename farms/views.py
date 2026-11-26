from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import render
from django.utils import timezone

from .access import visible_farms
from .models import Flock


@login_required
def dashboard(request):
    farms = visible_farms(request.user)
    flocks = Flock.objects.filter(
        status=Flock.Status.ACTIVE, house__farm__in=farms
    )

    today = timezone.localdate()
    on_today = Q(daily_logs__date=today)
    totals = flocks.aggregate(
        deaths=Sum('daily_logs__deaths', filter=on_today),
        culls=Sum('daily_logs__culls', filter=on_today),
        feed=Sum('daily_logs__feed_used_kg', filter=on_today),
        eggs=Sum('daily_logs__eggs_collected', filter=on_today),
    )

    stats = {
        'live_birds': sum(f.live_birds for f in flocks),
        'losses_today': (totals['deaths'] or 0) + (totals['culls'] or 0),
        'eggs_today': totals['eggs'] or 0,
        'feed_today': totals['feed'] or 0,
    }

    return render(request, 'dashboard.html', {
        'farms': farms.prefetch_related('houses__flocks'),
        'stats': stats,
    })