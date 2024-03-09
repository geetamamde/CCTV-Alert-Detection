from .models import PlanInformation
from django import forms


class PlanInformationForm(forms.ModelForm):
    class Meta:
        model = PlanInformation
        fields = ['number_of_cctvs', 'start_time', 'end_time', 'period', 'plan', 'user']