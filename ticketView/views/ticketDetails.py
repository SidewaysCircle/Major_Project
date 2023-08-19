from django.views.generic import DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from ..models import IncidentSolve
from ..forms import viewResolutionForm

from django.shortcuts import get_object_or_404

class incidentDetailsView(UserPassesTestMixin, DetailView):
    template_name = "ticketView.html"
    form_class = viewResolutionForm

    def test_func(self):
        return self.request.user.groups.filter(name='engineers').exists()

    def get_object(self, queryset=None):
        incident_id = self.kwargs.get("pk")
        return get_object_or_404(IncidentSolve, id=incident_id)
    
    def form_valid(self, form):
        return super(incidentDetailsView, self).form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response