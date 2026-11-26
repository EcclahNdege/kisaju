from django import forms

from farms.access import visible_farms
from farms.models import Flock

from .models import DailyLog


class DateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, **kwargs):
        kwargs.setdefault('format', '%Y-%m-%d')
        super().__init__(**kwargs)


class DailyLogForm(forms.ModelForm):
    class Meta:
        model = DailyLog
        fields = (
            'flock', 'date', 'deaths', 'culls',
            'feed_used_kg', 'eggs_collected', 'avg_weight_kg', 'notes',
        )
        widgets = {
            'date': DateInput(),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['flock'].queryset = Flock.objects.filter(
            status=Flock.Status.ACTIVE,
            house__farm__in=visible_farms(user),
        ).select_related('house__farm')
        for name, field in self.fields.items():
            css = 'form-select' if name == 'flock' else 'form-control'
            field.widget.attrs.setdefault('class', css)
