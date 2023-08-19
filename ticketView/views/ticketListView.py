from django.contrib.auth.mixins import UserPassesTestMixin

from django.views.generic import ListView
from ..models import *

class incidentListView(UserPassesTestMixin, ListView):
    template_name = "ticketList.html"
    queryset = IncidentSolve.objects.all()
    context_object_name = "incidentList"

    def test_func(self):
        return self.request.user.groups.filter(name='engineers').exists()
