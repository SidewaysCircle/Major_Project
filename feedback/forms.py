from django import forms

from .models import FeedbackResolves
from feedback.models import FeedbackResolves

from django.core.exceptions import ValidationError

class editFeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackResolves
        fields = [
            'feedbackIncident',
            'feedbackResult',
            'feedbackDetail',
            'feedbackShow'
        ]

    def __init__(self, *args, **kwargs):
        super(editFeedbackForm, self).__init__(*args, **kwargs)
        self.fields['feedbackIncident'].disabled = True #Users don't need to edit this however they do need to see it
    
    def clean_feedbackDetail(self):
        allowedSpecChars = [" ", "," , "."] #Only basic punctuation needed in the feedback field
        detail = self.cleaned_data['feedbackDetail']
        if self.fieldIsNoneOrEmpty(detail): #Check to ensure the field is populated
            raise ValidationError("Please provide additional details")
        return detail
    
    def clean_feedbackShow(self): #Allows the feedback object to be seen in the list
        show = self.cleaned_data['feedbackShow']
        return not show

    
    @staticmethod
    def fieldIsNoneOrEmpty(field) -> bool:
        return field is None or field == ""


class createFeedbackForm(forms.ModelForm): #None of these form fields are taken from the form they are created at
    class Meta:
        model = FeedbackResolves
        fields = [
            #'feedbackIncident',
            #'feedbackResult',
            #'feedbackDetail',
            #'feedbackShow'
        ]

    def form_valid(self, form, fkIncident):
        feedback = FeedbackResolves(
            feedbackIncident = fkIncident,
            feedbackResult = True,
            feedbackDetail = '',
            feedbackShow = False
        )
        feedback.save()

