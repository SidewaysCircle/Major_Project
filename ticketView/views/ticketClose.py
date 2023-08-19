from django.http import HttpResponseRedirect
from django.views.generic import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from ..models import IncidentSolve
from ..forms import hideIncidentForm

from feedback.forms import editFeedbackForm
from feedback.models import FeedbackResolves

from django.urls import reverse

class ticketCloseView(UserPassesTestMixin, UpdateView):
    model = FeedbackResolves
    second_model = IncidentSolve

    template_name = "feedbackCreate.html"

    form_class = editFeedbackForm
    second_form_class = hideIncidentForm

    def test_func(self):
        return self.request.user.groups.filter(name='engineers').exists()

    def get_context_data(self, **kwargs):
        context = super(ticketCloseView, self).get_context_data(**kwargs)
        feedback_id = self.kwargs.get("pk")
        feedback = self.model.objects.get(pk=feedback_id)
        incident = self.second_model.objects.get(id = feedback.feedbackIncident_id)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=incident)
        context['id'] = feedback_id
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        feedback_id = kwargs['pk']
        feedback = self.model.objects.get(pk=feedback_id)
        incident = self.second_model.objects.get(id = feedback.feedbackIncident_id)
        form = self.form_class(request.POST, instance=feedback)
        form2 = self.second_form_class(request.POST , instance=incident)

        if form.is_valid() and form2.is_valid():
            form.save()
            form2.instance.incidentShow = False
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))
    
    def get_success_url(self, **kwargs):
        return reverse("index")
