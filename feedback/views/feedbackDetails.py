from django.views.generic import DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from ..models import FeedbackResolves
from ..forms import editFeedbackForm

from django.shortcuts import get_object_or_404

class feedbackDetailsView(UserPassesTestMixin, DetailView):
    template_name = "feedbackView.html"
    form_class = editFeedbackForm

    def test_func(self):
        return self.request.user.is_superuser

    def get_object(self, queryset=None):
        feedback_id = self.kwargs.get("pk")
        return get_object_or_404(FeedbackResolves, pk=feedback_id)
    
    def form_valid(self, form):
        return super(feedbackDetailsView, self).form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response