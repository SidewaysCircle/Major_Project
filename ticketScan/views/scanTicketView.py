from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect

from ..models import *
from ticketView.models import IncidentSolve
from feedback.models import FeedbackResolves

from ..forms import *
from ticketView.forms import createScannedIncident
from feedback.forms import createFeedbackForm

class scanTicketView(LoginRequiredMixin, CreateView):
    model = ResolutionPath
    second_model = IncidentSolve
    third_model = FeedbackResolves

    template_name = "resolutionPathFindEntry.html"

    form_class = findResolutionForm
    second_form_class = createScannedIncident
    third_form_class = createFeedbackForm

    incident_queryset = IncidentSolve.objects.all()

    def get_context_data(self, **kwargs):
        context = super(scanTicketView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class()
        if 'form3' not in context:
            context['form3'] = self.third_form_class()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        
        incident = None
        feedback = None
        
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST, instance = incident)
        form3 = self.third_form_class(request.POST, instance = feedback)
        
        form2.instance.incidentNumber = request.POST.get('incidentNumber')
        form2.instance.incidentAddDetail = request.POST.get('incidentAddDetail')

        if form.is_valid():
            if form2.is_valid():
                resolution = self.model.objects.get(incidentType = request.POST.get('incidentType'),
                                            incidentArea = request.POST.get('incidentArea'), 
                                            incidentDetail = request.POST.get('incidentDetail'))

                form2.form_valid(form2, resolution)

                fkIncident = self.second_model.objects.get(incidentNumber = request.POST.get('incidentNumber'))

                form3.form_valid(form3, fkIncident)

                return HttpResponseRedirect(self.get_success_url())
            return self.render_to_response(self.get_context_data(form=form, form2=form2))
        return self.render_to_response(self.get_context_data(form=form, form2=form2))

    def load_areas(request):
        platform_id = request.GET.get('incidentType')
        areas = ProblemArea.objects.filter(fkPlatformName=platform_id).order_by('areaName')
        return render(request, 'incidentArea_dropdown_list_options.html', {'incidentAreas': areas})
    
    def load_errors(request):
        area_id = request.GET.get('incidentArea')
        errors = ProblemError.objects.filter(fkAreaName=area_id).order_by('errorDetail')
        return render(request, 'incidentError_dropdown_list_options.html', {'incidentErrors': errors})
    
    def get_success_url(self, **kwargs):
        return reverse("index")
    
    
    