from django.contrib import admin
from .models import ResolutionPath, ProblemPlatform, ProblemArea, ProblemError

# Register your models here.
admin.site.register(ResolutionPath)
admin.site.register(ProblemPlatform)
admin.site.register(ProblemArea)
admin.site.register(ProblemError)