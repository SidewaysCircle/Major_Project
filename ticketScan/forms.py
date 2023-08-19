from django import forms
from django.core.exceptions import ValidationError

from .models import ResolutionPath, ProblemArea, ProblemError

class findResolutionForm(forms.ModelForm):
    class Meta:
        model = ResolutionPath
        fields = [
            'incidentType',
            'incidentArea',
            'incidentDetail',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['incidentArea'].queryset = ProblemArea.objects.none()
        self.fields['incidentDetail'].queryset = ProblemError.objects.none()

        if 'incidentType' in self.data:
            try:
                platform_id = int(self.data.get('incidentType'))
                self.fields['incidentArea'].queryset = ProblemArea.objects.filter(fkPlatformName=platform_id).order_by('areaName')
            except (ValueError, TypeError, ValidationError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['incidentArea'].queryset = self.instance.incidentArea.areaName.order_by('areaName')

        if 'incidentArea' in self.data:
            try:
                area_id = int(self.data.get('incidentArea'))
                self.fields['incidentDetail'].queryset = ProblemError.objects.filter(fkAreaName=area_id).order_by('errorDetail')
            except (ValueError, TypeError, ValidationError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['incidentDetail'].queryset = self.instance.incidentDetail.errorDetail.order_by('errorDetail')

    def clean_incidentType(self):
        type = self.cleaned_data['incidentType']
        if self.fieldIsNoneOrEmpty(type):
            raise ValidationError("Please provide the type of issue you are having.")
        return type
    
    def clean_incidentArea(self):
        area = self.cleaned_data['incidentArea']
        if self.fieldIsNoneOrEmpty(area):
            raise ValidationError("Please provide the area which the issue is affecting.")
        return area
    
    def clean_incidentDetail(self):
        detail = self.cleaned_data['incidentDetail']
        if self.fieldIsNoneOrEmpty(detail):
            raise ValidationError("Please provide the error message which you are seeing.")
        return detail
    
    @staticmethod
    def fieldIsNoneOrEmpty(field) -> bool:
        return field is None or field == ""