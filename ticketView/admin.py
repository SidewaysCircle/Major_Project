from django.contrib import admin
from .models import IncidentSolve

# Register your models here.

class IncidentSolveAdmin(admin.ModelAdmin):
    pass

admin.site.register(IncidentSolve, IncidentSolveAdmin)