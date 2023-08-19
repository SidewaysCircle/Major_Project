from django import forms
from .models import IncidentSolve
from ticketScan.models import ResolutionPath

from django.core.exceptions import ValidationError

class createScannedIncident(forms.ModelForm):
    class Meta:
        model = IncidentSolve
        fields = [
            'incidentNumber',
            #'incidentResolutionPath',
            'incidentAddDetail'
            #'incidentShow'
        ]

    incidentNumber = forms.CharField(max_length=15, required=False)
    incidentAddDetail = forms.CharField(max_length=125, required=False)

    def clean_incidentNumber(self):
        number = self.cleaned_data['incidentNumber'].upper()
        scannedTickets = IncidentSolve.objects.filter(incidentNumber = number)
        if self.fieldIsNoneOrEmpty(number):
            raise ValidationError("INC number is required")
        if len(scannedTickets) != 0:
            raise ValidationError("This ticket has already been scanned")
        if number[:8] != "INC00000":
            raise ValidationError("This is not a valid INC number")
        if not self.fieldIsNumeric(number[8:]):
            raise ValidationError("This is not a valid INC number")
        if len(number) != 15:
            raise ValidationError("This is not a valid INC number")
        return number
    
    def clean_incidentAddDetail(self):
        allowedSpecChars = [" ", "," , "."]
        detail = self.cleaned_data['incidentAddDetail']

        alphaNumDetail = str(detail)
        for specChar in allowedSpecChars:
            alphaNumDetail = alphaNumDetail.replace(specChar, "")

        if self.fieldIsNoneOrEmpty(detail):
            raise ValidationError("Please provide additional details.")
        if not self.fieldIsAlphanumeric(alphaNumDetail):
            raise ValidationError("No special characters in the additional information box.")
        return detail

    def form_valid(self, form, resolution):
        incident = IncidentSolve(
            incidentNumber = form.cleaned_data['incidentNumber'],
            incidentResolutionPath = resolution,
            incidentAddDetail = form.cleaned_data['incidentAddDetail'],
            incidentShow = True
        )
        incident.save()

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response

    @staticmethod
    def fieldIsNumeric(field) -> bool:
        #Verify that field is numeric
        return field.isnumeric()
    
    @staticmethod
    def fieldIsNoneOrEmpty(field) -> bool:
        return field is None or field == ""
    
    @staticmethod
    def fieldIsAlphanumeric(field) -> bool:
        #Verify that field is alphanumeric
        return field.isalnum()

class viewResolutionForm(forms.ModelForm):
    class Meta:
        model = ResolutionPath
        fields = [
            'incidentType',
            'incidentArea',
            'incidentDetail',
            'incidentSuggestion',
            'incidentJustification'
        ]

class hideIncidentForm(forms.ModelForm):
    
    class Meta:
        model = IncidentSolve
        fields = [
            'incidentShow'
        ]