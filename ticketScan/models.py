from django.db import models
from django.urls import reverse

# Create your models here.

class ProblemPlatform(models.Model):
    platformName = models.CharField(max_length = 8)

    def __str__(self):
        return self.platformName
    
    def get_absolute_url(self):
        return reverse("incidentList")

class ProblemArea(models.Model):
    fkPlatformName = models.ForeignKey(ProblemPlatform, on_delete=models.DO_NOTHING)
    areaName = models.CharField(max_length=125)

    def __str__(self):
        return self.areaName
    
    def get_absolute_url(self):
        return reverse("incidentList")

class ProblemError(models.Model):
    fkAreaName = models.ForeignKey(ProblemArea, on_delete=models.DO_NOTHING)
    errorDetail = models.CharField(max_length=255)

    def __str__(self):
        return self.errorDetail
    
    def get_absolute_url(self):
        return reverse("incidentList")

class ResolutionPath(models.Model):
    incidentType = models.ForeignKey(ProblemPlatform, on_delete=models.DO_NOTHING)
    incidentArea = models.ForeignKey(ProblemArea, on_delete=models.DO_NOTHING)
    incidentDetail = models.ForeignKey(ProblemError, on_delete=models.DO_NOTHING)
    incidentSuggestion = models.CharField(max_length=125)
    incidentJustification = models.CharField(max_length=255)

    def __str__(self):
        ret = str(self.incidentType) + "," + str(self.incidentArea) + "," + str(self.incidentDetail) + "," + self.incidentSuggestion + "," + self.incidentJustification
        return ret

    def get_absolute_url(self):
        return reverse("index")
    
    def get_success_url(self):
        return reverse("index")
