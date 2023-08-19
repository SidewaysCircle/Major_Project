from django.db import models
from django.urls import reverse

from ticketScan.models import ResolutionPath
# Create your models here.

  
class IncidentSolve(models.Model):
    incidentNumber = models.CharField(max_length=15)
    incidentResolutionPath = models.ForeignKey(ResolutionPath, on_delete=models.DO_NOTHING)
    incidentAddDetail = models.CharField(max_length=125)
    incidentShow = models.BooleanField(default=True)

    def __str__(self):
        ret = self.incidentNumber
        return ret
    
    def get_absolute_url(self):
        return reverse("index")
    
    def get_success_url(self):
        return reverse("index")


    
  
