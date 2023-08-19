from django.urls import path

from .views.feedbackList import feedbackListView
from .views.feedbackDetails import feedbackDetailsView

urlpatterns = [
    path("", feedbackListView.as_view(), name = "feedbackList"),
    path("<int:pk>/view/", feedbackDetailsView.as_view(), name = "feedbackView"),
]