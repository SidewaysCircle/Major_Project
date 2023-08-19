from django.urls import path

from .views.ticketListView import incidentListView
from .views.ticketDetails import incidentDetailsView
from .views.ticketClose import ticketCloseView

urlpatterns = [
    path("", incidentListView.as_view(), name = "ticketList"),
    path("<int:pk>/view/", incidentDetailsView.as_view(), name = "incidentView"),
    path("<int:pk>/close/", ticketCloseView.as_view(), name = "ticketClose" )
]