from django.db import models
from django.urls import reverse

from ticketView.models import IncidentSolve

class FeedbackResolves(models.Model):
    feedbackIncident = models.OneToOneField(IncidentSolve, on_delete=models.CASCADE, primary_key= True)
    feedbackResult = models.BooleanField(default=True) #True means the resolution worked
    feedbackDetail = models.CharField(max_length=256, blank=True, null=True)
    feedbackShow = models.BooleanField(default=False)

    def __str__(self):
        ret = str(self.feedbackDetail)
        return ret
    
    def get_absolute_url(self):
        return reverse("index")
    
    def get_success_url(self):
        return reverse("index")