from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView
from ..models import *

class feedbackListView(UserPassesTestMixin, ListView):
    template_name = "feedbackList.html"
    queryset = FeedbackResolves.objects.all()
    context_object_name = "feedbackList"

    def test_func(self):
        return self.request.user.is_superuser